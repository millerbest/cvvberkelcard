from ..models import PlayerCard


def calculate_statistics():
    total_cards = PlayerCard.objects.count()
    collected_cards = PlayerCard.objects.filter(is_collected=True).count()
    uncollected_cards = total_cards - collected_cards
    collection_rate = (collected_cards / total_cards) * 100 if total_cards > 0 else 0
    print(f"Total Cards: {total_cards}")
    print(f"Collected Cards: {collected_cards}")
    print(f"Uncollected Cards: {uncollected_cards}")
    print(f"Collection Rate: {collection_rate:.2f}%")
    return {
        "total_cards": total_cards,
        "collected_cards": collected_cards,
        "uncollected_cards": uncollected_cards,
        "collection_rate": f"{collection_rate:.2f}%",
    }


def calculate_statistics_by_team():
    teams = PlayerCard.objects.values_list("team__name", flat=True).distinct()
    team_stats = {}

    for team in teams:
        total_cards = PlayerCard.objects.filter(team__name=team).count()
        collected_cards = PlayerCard.objects.filter(
            team__name=team, is_collected=True
        ).count()
        uncollected_cards = total_cards - collected_cards
        collection_rate = (
            (collected_cards / total_cards) * 100 if total_cards > 0 else 0
        )

        team_stats[team] = {
            "total_cards": total_cards,
            "collected_cards": collected_cards,
            "uncollected_cards": uncollected_cards,
            "collection_rate": f"{collection_rate:.2f}%",
        }
    # pretty print the team stats
    for team, stats in team_stats.items():
        print(f"Team: {team}")
        print(f"  Total Cards: {stats['total_cards']}")
        print(f"  Collected Cards: {stats['collected_cards']}")
        print(f"  Uncollected Cards: {stats['uncollected_cards']}")
        print(f"  Collection Rate: {stats['collection_rate']}")
        print()
    return team_stats


def print_all():
    print("Overall Statistics:")
    calculate_statistics()
    print("\nStatistics by Team:")
    calculate_statistics_by_team()
