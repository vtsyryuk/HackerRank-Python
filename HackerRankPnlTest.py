import pickle
import unittest
from nose.tools import assert_equal


class HackerRankPnlTest(unittest.TestCase):
    @staticmethod
    def read_data_from_single_string(input_string):
        """
        Use this function to read the string in the input file
        """
        ordered_keys = ['closes', 'positions', 'currency_mapping', 'fx_rates']
        hex_strings = input_string.split()
        assert len(ordered_keys) == len(hex_strings)  # If not, data is malformed
        data = {}
        for i, k in enumerate(ordered_keys):
            data[k] = pickle.loads(bytes.fromhex(hex_strings[i]))
        return data

    @staticmethod
    def calculate_pnl(closes, positions, currency_mapping, fx_rates):
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
        # #1 priority is test case completion, #2 is code readability gauged by an actual person reading it.
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

    def test_pnl(self):
        input_str1 = "80037d710028580a000000323031392d30362d3033710158060000003030323537347102867103474015eb851eb851ec680158030000003332367104867105473fe999999999999a680158050000004d4a4553237106867107473fc3333333333333680158050000004e45522d527108867109474002147ae147ae1468015808000000534c462e50522e42710a86710b474035f33333333333580a000000323031392d30362d3034710c680286710d474015eb851eb851ec680c680486710e473fe8a3d70a3d70a4680c680686710f473fc3333333333333680c6808867110474001eb851eb851ec680c680a867111474035a8f5c28f5c29580a000000323031392d30362d303571126802867113474015b851eb851eb868126804867114473fe800000000000068126806867115473fc3333333333333681268088671164740028f5c28f5c28f6812680a867117474035a66666666666580a000000323031392d30362d303671186802867119474015f5c28f5c28f66818680486711a473fe80000000000006818680686711b473fc33333333333336818680886711c4740035c28f5c28f5c6818680a86711d474035a8f5c28f5c29580a000000323031392d30362d3037711e680286711f474015f5c28f5c28f6681e6804867120473fe8000000000000681e6806867121473fc3333333333333681e6808867122474003d70a3d70a3d7681e680a867123474035b851eb851eb8752e"
        input_str2 = "80037d710028580a000000323031392d30362d30337101580600000030303235373471028671034a86ffffff68015808000000534c462e50522e4271048671054d7202580a000000323031392d30362d3034710658050000004d4a45532371078671084d2901580a000000323031392d30362d30357109680286710a4b516809680486710b4b1e580a000000323031392d30362d3036710c680486710d4b64580a000000323031392d30362d3037710e680786710f4b82752e"
        input_str3 = "80035d710028580600000030303235373471015803000000434e597102867103580300000033323671045803000000484b44710586710658050000004d4a45532371075803000000455552710886710958050000004e45522d52710a5803000000544842710b86710c5808000000534c462e50522e42710d5803000000434144710e86710f652e"
        input_str4 = "80037d71005808000000555344787261746571017d710228580a000000323031392d30362d303371035803000000434e597104867105473fc286632cd8527d68035803000000484b447106867107473fc05604d6b6d5f5680358030000004555527108867109473ff1ec226809d49568035803000000544842710a86710b473fa02d9f6029b35768035803000000434144710c86710d473fe7bebac9b80455580a000000323031392d30362d3034710e680486710f473fc28465d8300ee4680e6806867110473fc0528d7280635a680e6808867111473ff1f9096bb98c7e680e680a867112473fa057429c03c497680e680c867113473fe7d400f4001489580a000000323031392d30362d303571146804867115473fc286efc164d5eb68146806867116473fc05360ec22814b68146808867117473ff204ea4a8c154d6814680a867118473fa055422b52eb566814680c867119473fe7e13469430189580a000000323031392d30362d3036711a680486711b473fc281b98e533c67681a680686711c473fc0537c3732385b681a680886711d473ff20d4fdf3b645a681a680a86711e473fa056ed2b2e48d9681a680c86711f473fe7e883355f64dc580a000000323031392d30362d303771206804867121473fc281b98e533c6768206806867122473fc052ecf11af69468206808867123473ff223d70a3d70a46820680a867124473fa052426d83b2fb6820680c867125473fe8170ca200264375732e"
        text = "\n".join([input_str1, input_str2, input_str3, input_str4])
        data = self.read_data_from_single_string(text)
        assert_equal(63.44, self.calculate_pnl(data['closes'], data['positions'], data['currency_mapping'], data['fx_rates']))


if __name__ == '__main__':
    unittest.main()
