ISSUE_KEYWORDS = {
    "交通": ["停車", "違停", "號誌", "交通", "機車", "汽車"],
    "道路": ["坑洞", "柏油", "路面", "施工"],
    "環境": ["垃圾", "髒亂", "異味", "清潔"],
    "人行": ["人行道", "斑馬線", "無障礙"],
    "公共安全": ["路燈", "照明", "危險"],
}


def classify(text: str):
    for category, keywords in ISSUE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return category
    return "其他"


if __name__ == "__main__":
    sample = "市場周邊停車問題嚴重"
    print(classify(sample))
