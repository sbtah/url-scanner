class Url:
    """
    Class representing an Url object that is being verified.
    This object main role is to store responses from APIs
        and calculate certain values from them.
    Note:
        Initially I wanted to use pydantic model for this task,
        but later, I decided that I want hash-ability for this object
        ( fast membership tests )
    """
    def __init__(
        self,
        *,
        value: str,
        google_data: dict | None = None,
        virus_data: dict | None = None,
        browser_data: dict | None = None,
        probe_data: dict | None = None,
    ) -> None:
        """
        :param value:
        :param google_data:
        :param virus_data:
        :param browser_data:
        :param probe_data:
        """
        self.value: str = value
        self.google_data: dict | None = google_data
        self.virus_data: dict | None = virus_data
        self.browser_data: dict | None = browser_data
        self.probe_data: dict | None = probe_data

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

    # Virus API calculated.
    @property
    def virus_phishing_score(self) -> int | None:
        """
        """
        if self.virus_data is None:
            return None
        analysis_stats: dict | None = self.virus_data.get('data', {}).get('attributes', {}).get('last_analysis_stats')
        if analysis_stats is None:
            return None
        return int(analysis_stats['malicious'])

    @property
    def is_phishing(self):
        """"""
        if self.virus_phishing_score is None:
            return None
        return self.virus_phishing_score > 3

    @property
    def virus_harmless_score(self) -> int | None:
        """
        """
        if self.virus_data is None:
            return None
        analysis_stats: dict | None = self.virus_data.get('data', {}).get('attributes', {}).get('last_analysis_stats')
        if analysis_stats is None:
            return None
        return int(analysis_stats['harmless'])

    @property
    def virus_undetected_score(self) -> int | None:
        """
        """
        if self.virus_data is None:
            return None
        analysis_stats: dict | None = self.virus_data.get('data', {}).get('attributes', {}).get('last_analysis_stats')
        if analysis_stats is None:
            return None
        return int(analysis_stats['undetected'])

    @property
    def virus_suspicious_score(self) -> int | None:
        """
        """
        if self.virus_data is None:
            return None
        analysis_stats: dict | None = self.virus_data.get('data', {}).get('attributes', {}).get('last_analysis_stats')
        if analysis_stats is None:
            return None
        return int(analysis_stats['suspicious'])

    @property
    def virus_error(self) -> None | str:
        """"""
        if self.virus_data is None:
            return None
        error_data: dict | None = self.virus_data.get('error', {}).get('code', {})
        if error_data is None:
            return None
        return str(error_data)

    @property
    def google_threat_types(self) -> list | None:
        """"""
        if self.google_data is None:
            return None
        matches: list | None = self.google_data.get('matches')
        if matches is None:
            return None
        return [str(data['threatType']) for data in matches]

    # Google API calculated.
    @property
    def google_platform_types(self) -> list | None:
        """"""
        if self.google_data is None:
            return None
        matches: list | None = self.google_data.get('matches')
        if matches is None:
            return None
        return [str(data['platformType']) for data in matches]

    @property
    def google_threats(self) -> list | None:
        """"""
        if self.google_data is None:
            return None
        matches: list | None = self.google_data.get('matches')
        if matches is None:
            return None
        return [dict(data['threat']) for data in matches]

    # Probe calculated.
    @property
    def probe_status(self) -> str | None:
        """"""
        if self.probe_data is None:
            return None
        status: str | None = self.probe_data.get('status')
        return str(status)

    @property
    def probe_is_alive(self) -> bool | None:
        """
        Indicator that page returned a status code in either 200 or 300 range.
        :return: Bool or None
        """
        if self.probe_data is None:
            return None
        alive = self.probe_status.startswith('2') or self.probe_status.startswith('3')
        return alive

    # Browser checks.
    @property
    def browser_status(self) -> str | None:
        """"""
        if self.browser_data is None:
            return None
        status: str = self.browser_data['status']
        return str(status)

    @property
    def browser_is_alive(self) -> bool | None:
        """"""
        if self.browser_data is None:
            return None
        alive = self.browser_status.startswith('2') or self.browser_status.startswith('3')
        return alive

    @property
    def screenshot(self) -> str | None:
        """"""
        if self.browser_data is None:
            return None
        screenshot_name: str = self.browser_data['screenshot']
        return str(screenshot_name)

    @property
    def blocked(self) -> bool | None:
        """"""
        if self.browser_data is None:
            return None
        blocked: bool = self.browser_data['blocked']
        return blocked

    def to_dict(self):
        return {
            'value': self.value,
            'probe_status': self.probe_status,
            'probe_is_alive': self.probe_is_alive,
            'browser_status': self.browser_status,
            'browser_is_alive': self.browser_is_alive,
            'screenshot': self.screenshot,
            'webpage-blocked': self.blocked,
        }