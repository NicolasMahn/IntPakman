# Test Data
address = ["eStraße 10", "aStraße 4", "bStraße 2", "eStraße 11", "aStraße 1", "cStraße 4"]
route = ["aStraße 1", "bStraße 2", "aStraße 4", "cStraße 4", "eStraße 10", "eStraße 11"]

address_right_order = []
address.sort()


# binary search algorithm.
def binary_search(address_list, route_element):
    lower_bound = 0
    upper_bound = len(address_list)

    while lower_bound < upper_bound:

        mid_index = (lower_bound + upper_bound) // 2
        mid_index = int(mid_index)

        if address_list[mid_index] == route_element:
            return mid_index
        elif address_list[mid_index] < route_element:
            lower_bound = mid_index + 1
        else:
            upper_bound = mid_index


for x in route:
    address_right_order.append(address[binary_search(address, x)])

print(address_right_order)
