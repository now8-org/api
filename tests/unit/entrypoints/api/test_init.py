from now8_api.entrypoints.api import _return_msg


class TestReturnMsg:
    def test_return_msg(self):
        result = _return_msg("test_msg", "test_key")

        assert result == {"test_key": "test_msg"}
