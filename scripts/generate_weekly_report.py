from aggregation.weekly_report import generate


def main():
    path = generate()
    print(f"Report written to {path}")


if __name__ == "__main__":
    main()
