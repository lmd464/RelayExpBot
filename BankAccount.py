class BankAccount:

    def __init__(self):
        self.account_txt = open("bank_account.txt", 'r')
        self.account_dict = {}
        while True:
            line = self.account_txt.readline()
            if not line:
                break
            line = line.split(" : ")
            self.account_dict[line[0].strip()] = line[1].strip()

        self.account_txt.close()

    def get_bank_account(self, name):
        acc = self.account_dict.get(name)
        if acc is None:
            return "등록된 정보가 없습니다."
        else:
            return name + " : " + acc

    def add_bank_account(self, name, acc):
        self.account_dict[name] = acc

        # 파일에 추가
        self.account_txt = open("bank_account.txt", 'a')
        new_acc = name + " : " + acc
        self.account_txt.write("\n" + new_acc)
        self.account_txt.close()
        return "계좌 목록에 추가되었습니다."

    def delete_bank_account(self, name):
        self.account_dict.pop(name, None)

        # 새 텍스트파일로 갱신
        self.account_txt = open("bank_account.txt", 'w')
        for key, value in self.account_dict.items():
            self.account_txt.write(key + " : " + value + '\n')
        self.account_txt.close()
        return "계좌 정보가 삭제되었습니다."


