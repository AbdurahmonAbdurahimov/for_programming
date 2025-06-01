
def test_check_threshold_warning_logic():
    def is_below_threshold(quantity, threshold):
        return quantity < threshold

    assert is_below_threshold(50, 100) == True
    assert is_below_threshold(150, 100) == False
