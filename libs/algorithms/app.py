# input
# a, b = [s for s in input("").split()]
a = int(input(""))

# libs
def from_decimal(value: int, base: int) -> str:
    res = ""
    while value > 0:
        # calculate remainder from dividing value by base
        reminder = value % base
        # handle reminder
        res = str(reminder) + res
        # divide value by base without a remainder
        value = value // base
    return res


def to_decimal(value: str, base: int) -> int:
    res = 0
    for i in range(len(value)):
        # digit
        digit = int(value[i])
        # digit index
        digit_index = len(value) - i - 1
        # calculate and add to the res
        res += digit * base ** digit_index
    return res


# code
def b(value: int) -> int:
    return to_decimal(from_decimal(value, 2)[::-1], 2)


result = b(a)
#

print(result)
