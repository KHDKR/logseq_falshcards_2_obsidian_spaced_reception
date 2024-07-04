import re
from datetime import datetime, timedelta


# 定义转换函数
def convert_logseq_to_anki_format(logseq_data):
    # 定义转换比例因子 k
    k = 1000
    base_ease = 230  # Anki的容易度基数，对应Logseq的2.5

    # 正则表达式，用于匹配整个卡片块
    card_pattern = re.compile(r"^-\s+.*?(?=\n-\s+|\Z)", re.MULTILINE | re.DOTALL)

    # 用于存储所有卡片的字符串
    all_cards = []

    # 分割数据为单独的卡片
    cards = card_pattern.findall(logseq_data)
    for card in cards:
        # 使用字符串方法提取属性
        title_match = re.match(r"^-\s+(.*?)(?=\s#|$)", card.split("\n")[0])
        title = title_match.group(1).strip() if title_match else "Untitled"
        properties = {}
        for line in card.split("\n"):
            line = line.strip()
            if "::" in line:
                key, value = line.split("::", 1)
                properties[key.strip()] = value.strip()

        # 从属性字典中获取标题，如果没有，则使用默认标题
        # title = properties.get("card-title", "Untitled")

        # 计算Anki的容易度值
        logseq_ease_factor = properties.get("card-ease-factor", 2.5)
        anki_ease = base_ease - (2.5 - float(logseq_ease_factor)) * (base_ease / 2.5)

        # 根据评分调整间隔
        last_score = int(properties.get("card-last-score", 3))
        new_interval_multiplier = (
            1.3 if last_score == 3 else 1.0 if last_score == 2 else 0.5
        )

        # 计算新间隔
        old_interval = float(properties.get("card-last-interval", 1))
        new_interval = old_interval * (anki_ease / 100) * new_interval_multiplier
        if new_interval < 0:
            new_interval = 0

        # 计算新的复习日期
        # last_reviewed = datetime.fromisoformat(
        # properties["card-last-reviewed"].rstrip("Z")
        # )
        # new_next_schedule = last_reviewed + timedelta(days=new_interval)
        last_reviewed_date = datetime.strptime(
            properties["card-last-reviewed"], "%Y-%m-%dT%H:%M:%S.%fZ"
        ).date()
        new_next_schedule = last_reviewed_date + timedelta(days=new_interval)

        # 提取卡片内容
        contents = [
            line.strip()
            for line in card.split("\n")
            if line.strip().startswith("-") and not line.strip().startswith("--")
        ]
        i = 1
        for line in contents[1:]:
            contents[i] = line[2:]
            i += 1
        card_content_str = f"{title}\n?\n"
        card_content_str += "\n".join(contents[1:]) + "\n"

        # 构建SR格式注释
        sr_comment = (
            f"<!--SR:!{new_next_schedule.isoformat()},{int(new_interval)},230-->\n"
        )

        # 将转换后的卡片添加到列表
        all_cards.append(card_content_str + sr_comment)

    # 返回所有卡片的格式化字符串
    return "\n".join(all_cards)


# 示例Logseq卡片数据
logseq_data = """
- offspring #card #words
  card-last-interval:: 7.2
  card-repeats:: 3
  card-ease-factor:: 1.8
  card-next-schedule:: 2024-07-08T18:13:34.126Z
  card-last-reviewed:: 2024-07-01T14:13:34.126Z
  card-last-score:: 3
	- n 子女；子孙；后代；产物
- turnover #card #words
  card-last-interval:: 19.01
  card-repeats:: 4
  card-ease-factor:: 2.18
  card-next-schedule:: 2024-07-12T14:48:01.036Z
  card-last-reviewed:: 2024-06-23T14:48:01.036Z
  card-last-score:: 5
	- n 人事变更率；营业额
- nasty #card #words
  card-last-interval:: 15.05
  card-repeats:: 4
  card-ease-factor:: 1.94
  card-next-schedule:: 2024-07-08T15:48:47.997Z
  card-last-reviewed:: 2024-06-23T14:48:47.997Z
  card-last-score:: 3
	- a 不友好的；极差的；严重的
- poll #card #words
  card-last-interval:: 4
  card-repeats:: 2
  card-ease-factor:: 1.8
  card-next-schedule:: 2024-07-08T00:51:58.011Z
  card-last-reviewed:: 2024-07-04T00:51:58.012Z
  card-last-score:: 3
	- n 民意调查；选举投票
	- v 对……进行民意测验；获行（票数）
- wage #card #words
  card-last-interval:: 15.05
  card-repeats:: 4
  card-ease-factor:: 1.94
  card-next-schedule:: 2024-07-08T15:42:43.271Z
  card-last-reviewed:: 2024-06-23T14:42:43.271Z
  card-last-score:: 3
	- n 工资；发动（战争、战斗等）
- prey #card #words
  card-last-interval:: 22.65
  card-repeats:: 4
  card-ease-factor:: 2.42
  card-next-schedule:: 2024-07-16T06:05:37.283Z
  card-last-reviewed:: 2024-06-23T15:05:37.283Z
  card-last-score:: 3
	- 捕食；猎物
- toll #card #words
  card-last-interval:: 7.76
  card-repeats:: 3
  card-ease-factor:: 1.94
  card-next-schedule:: 2024-07-05T10:45:45.036Z
  card-last-reviewed:: 2024-06-27T16:45:45.036Z
  card-last-score:: 3
	- n ==损失；通行费；伤亡人数==
	- v 敲（钟）
"""
# 执行转换并打印结果
converted_data = convert_logseq_to_anki_format(logseq_data)
print(converted_data)
