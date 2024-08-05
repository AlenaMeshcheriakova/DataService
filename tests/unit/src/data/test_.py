
# TODO: What to tests:
# • Missing inputs
# • Duplicate inputs
# • Incorrect input types
# • Incorrect input order
# • Invalid input values
# • Huge inputs or outputs


# MOCK example 1
# @mock.patch("mod1.preamble", return_value="")
# def test_summer_c(mock_preamble):
#   assert "11" == mod2.summer(5,6)

# MOCK example 2
# @mock.patch("mod1.preamble")
# def test_caller_d(mock_preamble):
#     mock_preamble.return_value = ""
#     assert "11" == mod2.summer(5,6)

# MOCK example 3
# def test_summer_a():
#     with mock.patch("mod1.preamble", return_value=""):
#     assert "11" == mod2.summer(5,6)


# import os
# if os.get_env("UNIT_TEST"):
#     import fake_mod1 as mod1
# else:
#     import mod1