class HackerRankPnlCalculator(object):
    @staticmethod
    def calculate_pnl(closes: dict, positions: dict, currency_mapping: list, fx_rates: dict) -> float:
        """
        Parameters
        ----------
        closes : dict
            Prices of the instruments, format (date_str, ticker) : value
        positions : dict
            Positions entered, format (date_str, ticker) : value
        currency_mapping : list
            Currency mapping, format (ticker, currency_name)
        fx_rates : dict
            Currency rates for desired dates

        Returns
        -------
        float
            total profit (loss if negative) experienced by this position table, rounded to cents
        """
        # #1 priority is tests case completion, #2 is code readability gauged by an actual person reading it.
        # Please don't dwell on performance-related stuff, not the proper environment to do that.

        currency_dict = dict(currency_mapping)
        rates_mapping = {}
        for value in fx_rates.values():
            for (date, currency), rate in value.items():
                rates_mapping.setdefault(currency, [])
                rates_mapping[currency].append((date, rate))
        ticker_last_price = {}
        for (date, ticker), price in closes.items():
            currency = currency_dict[ticker]
            rate = dict(rates_mapping[currency])[date]
            ticker_last_price[ticker] = price * rate

        result = 0
        for (date, ticker), pos in positions.items():
            price = closes[(date, ticker)]
            last_price = ticker_last_price[ticker]
            currency = currency_dict[ticker]
            rate = dict(rates_mapping[currency])[date]
            result += (last_price - price * rate) * pos

        return round(result, 2)
