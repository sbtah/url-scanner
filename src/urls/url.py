class Url:
    """
    Object representing a validated url.
    """

    def __init__(
        self,
        *,
        value: str,
        google_data: dict | None = None,
        virus_data: dict | None = None,
        browser_data: dict | None = None,
        # virus_created_at: float | None = None,
        # virus_last_analyzed_at: float | None = None,
        # virus_last_analysis_stats: dict | None = None,
        # virus_score_harmless: int | None = None,
        # virus_score_malicious: int | None = None,
        # virus_score_suspicious: int | None = None,
        # virus_score_timeout: int | None = None,
        # virus_score_undetected: int | None = None,
    ):
        self.value: str = value
        self.google_data: dict | None = google_data
        self.virus_data: dict | None = virus_data
        self.browser_data: dict | None = browser_data
        # # Attributes Virus
        # # ['attributes']['first_submission_date']
        # self.virus_created_at: float | None = virus_created_at
        # # ['attributes']['last_analysis_date']
        # self.virus_last_analyzed_at: float | None = virus_last_analyzed_at
        # # ['attribute']['last_analysis_stats']
        # self.virus_last_analysis_stats: dict | None = virus_last_analysis_stats

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value

    def __hash__(self) -> int:
        return hash(str(self.value))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Url):
            return NotImplemented
        return self.value == other.value

    def serialize(self) -> dict:
        return self.__dict__
