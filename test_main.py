from main import add,sub

def test_add():
    assert add(1,2)==3
def test_add_neg():
    assert add(-1,-1)==-2
def test_sub():
    assert sub(7,5)==2
def test_sub_neg():
    assert sub(9,8)