def question_1_2():
    curr_sum, max_list = 0, [0, 0, 0]
    with open("input.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                curr_sum += int(line)
            else:
                for i in range(len(max_list)):
                    if curr_sum > max_list[i]:
                        max_list[i] = curr_sum
                        break
                curr_sum = 0
    print("Answer 1 =", max(max_list), "\nAnswer2 = ", sum(max_list))


if __name__ == "__main__":
    question_1_2()
