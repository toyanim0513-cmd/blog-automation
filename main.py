"""트렌드 기반 블로그 자동화 시스템 - 메인 실행 파일."""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import IntPrompt, Confirm

import config
from modules.trend_collector import TrendCollector
from modules.curiosity_engine import CuriosityEngine
from modules.title_generator import TitleGenerator
from modules.content_writer import ContentWriter
from modules.image_generator import ImageGenerator
from modules.blog_publisher import BlogPublisher
from modules.naver_auth import NaverAuth

console = Console()


def step1_collect_trends() -> list[dict]:
    """STEP 1: 트렌드 수집."""
    console.print("\n[bold cyan]🔍 트렌드 수집 중...[/]")
    collector = TrendCollector(config.NAVER_CLIENT_ID, config.NAVER_CLIENT_SECRET)
    trends = collector.collect_trends()

    # 카테고리별로 최신 뉴스 상위 5개 선택
    seen = set()
    top_trends = []
    for t in trends:
        if t["title"] not in seen and len(top_trends) < 10:
            seen.add(t["title"])
            top_trends.append(t)

    return top_trends


def step1_display_trends(trends: list[dict]) -> dict:
    """트렌드 목록 표시 및 선택."""
    table = Table(title="📊 오늘의 트렌드 TOP", show_lines=True)
    table.add_column("#", style="bold", width=4)
    table.add_column("카테고리", style="cyan", width=8)
    table.add_column("제목", width=50)

    category_icons = {"뉴스": "📰", "경제": "💰", "핫이슈": "🔥"}

    for i, t in enumerate(trends, 1):
        icon = category_icons.get(t["category"], "📌")
        table.add_row(str(i), f"{icon} {t['category']}", t["title"])

    console.print(table)

    choice = IntPrompt.ask("\n👉 글 쓸 주제를 선택하세요", choices=[str(i) for i in range(1, len(trends) + 1)])
    return trends[choice - 1]


def step2_extract_curiosity(article: dict) -> dict:
    """STEP 2: 궁금증 포인트 추출."""
    console.print("\n[bold yellow]🧠 궁금증 포인트 분석 중...[/]")
    engine = CuriosityEngine(config.OPENAI_API_KEY, config.AI_MODEL)
    curiosity = engine.extract(
        title=article["title"],
        description=article["description"],
        category=article["category"],
    )

    console.print(Panel(
        f"[bold]왜 화제?[/] {curiosity['why_trending']}\n"
        f"[bold]나에게 영향?[/] {curiosity['impact_on_me']}\n"
        f"[bold]앞으로?[/] {curiosity['future_outlook']}",
        title="분석 결과",
    ))

    return curiosity


def step3_generate_title(article: dict, curiosity: dict) -> str:
    """STEP 3: 제목 생성 및 선택."""
    console.print("\n[bold green]✍️ 제목 생성 중...[/]")
    gen = TitleGenerator(config.OPENAI_API_KEY, config.AI_MODEL)
    titles = gen.generate(
        title=article["title"],
        why_trending=curiosity["why_trending"],
        impact_on_me=curiosity["impact_on_me"],
    )

    console.print("\n[bold]━━ 제목 후보 ━━[/]")
    for i, t in enumerate(titles, 1):
        console.print(f"  [{i}] {t}")

    choice = IntPrompt.ask("\n👉 제목을 선택하세요", choices=["1", "2", "3"])
    return titles[choice - 1]


def step4_write_content(article: dict, blog_title: str, curiosity: dict) -> str:
    """STEP 4-6: 콘텐츠 생성."""
    console.print("\n[bold magenta]📝 콘텐츠 작성 중...[/]")
    writer = ContentWriter(config.OPENAI_API_KEY, config.AI_MODEL)
    return writer.write(
        title=article["title"],
        description=article["description"],
        category=article["category"],
        blog_title=blog_title,
        curiosity=curiosity,
    )


def step7_generate_images(blog_title: str, curiosity: dict) -> list[str]:
    """STEP 7: 이미지 생성."""
    console.print("\n[bold blue]🖼️ 이미지 생성 중...[/]")
    gen = ImageGenerator()

    images = []
    try:
        thumb = gen.generate_thumbnail(blog_title)
        images.append(thumb)
        console.print(f"  ✅ 썸네일: {thumb}")
    except Exception as e:
        console.print(f"  ⚠️ 썸네일 생성 실패: {e}")

    try:
        card = gen.generate_summary_card(curiosity["top3_questions"])
        images.append(card)
        console.print(f"  ✅ 요약카드: {card}")
    except Exception as e:
        console.print(f"  ⚠️ 요약카드 생성 실패: {e}")

    return images


def step8_preview_and_publish(blog_title: str, content: str, access_token: str) -> None:
    """STEP 8: 미리보기 및 발행."""
    console.print("\n[bold]━━ 미리보기 ━━[/]")
    console.print(Panel(content[:500] + "...", title=blog_title, subtitle="(일부만 표시)"))

    if not Confirm.ask("\n👉 발행하시겠습니까?"):
        console.print("[yellow]발행을 취소했습니다.[/]")
        return

    console.print("\n[bold cyan]🚀 네이버 블로그에 발행 중...[/]")
    publisher = BlogPublisher(access_token)
    result = publisher.publish(title=blog_title, content=content)

    if result:
        console.print(f"\n[bold green]✅ 발행 완료![/]")
    else:
        console.print("[bold red]❌ 발행에 실패했습니다. API 설정을 확인해주세요.[/]")


def main():
    console.print(Panel(
        "[bold]트렌드 기반 블로그 자동화 시스템[/]\n"
        '"이걸 왜 알아야 하는지 알려주는 콘텐츠"',
        style="bold cyan",
    ))

    # OAuth 로그인
    console.print("\n[bold cyan]🔑 네이버 OAuth 로그인...[/]")
    naver_auth = NaverAuth(
        config.NAVER_CLIENT_ID,
        config.NAVER_CLIENT_SECRET,
        config.NAVER_REDIRECT_URI,
    )
    access_token = naver_auth.login()
    console.print("[bold green]✅ 로그인 완료![/]")

    # STEP 1: 트렌드 수집
    trends = step1_collect_trends()
    if not trends:
        console.print("[red]트렌드를 수집하지 못했습니다. API 키를 확인해주세요.[/]")
        return

    article = step1_display_trends(trends)

    # STEP 2: 궁금증 포인트
    curiosity = step2_extract_curiosity(article)

    # STEP 3: 제목 생성
    blog_title = step3_generate_title(article, curiosity)

    # STEP 4-6: 콘텐츠 생성
    content = step4_write_content(article, blog_title, curiosity)

    # STEP 7: 이미지 생성
    step7_generate_images(blog_title, curiosity)

    # STEP 8: 미리보기 + 발행
    step8_preview_and_publish(blog_title, content, access_token)


if __name__ == "__main__":
    main()
