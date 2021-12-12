from now8_api.service.service import exclude


class TestFucntions:
    def test_exclude(self):
        original = {
            1: {
                "a": 1,
                "b": 2,
                "c": 3,
            },
            2: {
                "a": 4,
                "b": 5,
                "c": 6,
            },
        }
        result = exclude(dict_of_dicts=original, keys_to_exclude=["a", "b"])

        assert result == {
            1: {
                "c": 3,
            },
            2: {
                "c": 6,
            },
        }

    def test_exclude_none(self):
        original = {
            1: {
                "a": 1,
                "b": 2,
                "c": 3,
            },
            2: {
                "a": 4,
                "b": 5,
                "c": 6,
            },
        }
        result = exclude(dict_of_dicts=original, keys_to_exclude=[])

        assert result == original
