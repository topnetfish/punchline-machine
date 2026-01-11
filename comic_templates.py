# comic_templates.py
# 四格漫画主题模板库（完整复用你提供的内容）
COMIC_TEMPLATES = {
    # 1. 生活日常类
    "生活日常": {
        "居家日常": {
            "sub_topic": "亲子搞笑互动",
            "funny_example": "妈妈让孩子洗碗，孩子用洗碗机 “偷懒”，最后妈妈哭笑不得",
            "default_title": "偷懒的洗碗方式",
            "default_topic": "居家·亲子·搞笑偷懒"
        },
        "宠物趣事": {
            "sub_topic": "猫狗的奇葩行为",
            "funny_example": "猫咪偷喝主人的奶茶，被抓包后装无辜，最后打翻杯子",
            "default_title": "偷喝奶茶的猫咪",
            "default_topic": "宠物·搞笑·拆家日常"
        },
        "合租生活": {
            "sub_topic": "室友的神操作",
            "funny_example": "室友囤零食藏在衣柜，被发现后借口 “防过期”",
            "default_title": "藏零食的室友",
            "default_topic": "合租·搞笑·零食大战"
        },
        "外卖/做饭": {
            "sub_topic": "厨房翻车现场",
            "funny_example": "学做网红菜，结果把锅烧糊，最后点外卖收尾",
            "default_title": "翻车的网红菜",
            "default_topic": "做饭·翻车·外卖救星"
        }
    },
    # 2. 职场打工人类
    "职场打工": {
        "摸鱼翻车": {
            "sub_topic": "假装工作实际摸鱼",
            "funny_example": "上班刷短视频，老板突然走到身后，秒切工作页面却切错成购物页",
            "default_title": "摸鱼翻车现场",
            "default_topic": "职场·摸鱼·社死瞬间"
        },
        "会议吐槽": {
            "sub_topic": "无效会议名场面",
            "funny_example": "会议开 1 小时没结论，最后老板说 “散会，下次再聊”",
            "default_title": "无效会议天花板",
            "default_topic": "职场·会议·无效沟通"
        },
        "需求改改改": {
            "sub_topic": "产品/客户改需求",
            "funny_example": "客户说 “就改一点点”，结果改了 10 版又回到第一版",
            "default_title": "改到崩溃的需求",
            "default_topic": "职场·需求·反复横跳"
        },
        "加班日常": {
            "sub_topic": "花式摸鱼加班",
            "funny_example": "加班时假装敲代码，实际在写小说，被同事拆穿",
            "default_title": "加班摸鱼写小说",
            "default_topic": "职场·加班·摸鱼技巧"
        }
    },
    # 3. 校园类
    "校园": {
        "小学趣味": {
            "sub_topic": "课间小游戏翻车",
            "funny_example": "玩 “石头剪刀布” 输了，被罚表演，结果紧张忘词",
            "default_title": "表演翻车的课间游戏",
            "default_topic": "校园·小学·课间趣事"
        },
        "高中日常": {
            "sub_topic": "晚自习摸鱼",
            "funny_example": "晚自习偷偷看漫画，被老师发现，谎称 “在看作文素材”",
            "default_title": "晚自习偷看漫画",
            "default_topic": "校园·高中·晚自习摸鱼"
        },
        "大学摆烂": {
            "sub_topic": "早八逃课/食堂踩雷",
            "funny_example": "为了早八课定 3 个闹钟，最后还是睡过头，谎称 “堵车”",
            "default_title": "早八课的摆烂日常",
            "default_topic": "校园·大学·早八逃课"
        },
        "师生互动": {
            "sub_topic": "老师的神回复",
            "funny_example": "学生问 “作业能不交吗”，老师答 “可以，我也能不批改”",
            "default_title": "老师的神级回复",
            "default_topic": "校园·师生·搞笑互动"
        }
    },
    # 4. 趣味脑洞类
    "趣味脑洞": {
        "谐音梗笑话": {
            "sub_topic": "汉字/词语谐音",
            "funny_example": "问：什么门永远关不上？答：球门（配四格反转画面）",
            "default_title": "永远关不上的门",
            "default_topic": "脑洞·谐音梗·趣味问答"
        },
        "动物拟人": {
            "sub_topic": "小动物的职场/校园",
            "funny_example": "熊猫上班摸鱼吃竹子，被 “老板”（饲养员）抓包",
            "default_title": "摸鱼的熊猫打工人",
            "default_topic": "脑洞·动物·职场拟人"
        },
        "反套路鸡汤": {
            "sub_topic": "毒鸡汤反转",
            "funny_example": "第一格：“努力就会成功”，最后一格：“努力不一定成功，但不努力真的很舒服”",
            "default_title": "反套路毒鸡汤",
            "default_topic": "脑洞·鸡汤·反套路"
        },
        "星座趣味": {
            "sub_topic": "星座性格反差",
            "funny_example": "处女座整理桌面，结果越整理越乱，最后摆烂",
            "default_title": "摆烂的处女座",
            "default_topic": "脑洞·星座·性格反差"
        }
    },
    # 5. 节日/季节类
    "节日季节": {
        "节日吐槽": {
            "sub_topic": "春节催婚/中秋吃月饼",
            "funny_example": "春节被亲戚催婚，谎称 “已经有对象了”，结果被拆穿",
            "default_title": "春节催婚翻车记",
            "default_topic": "节日·春节·催婚吐槽"
        },
        "季节趣事": {
            "sub_topic": "夏天怕热/冬天赖床",
            "funny_example": "夏天开空调盖被子，被妈妈吐槽 “浪费电”",
            "default_title": "夏天的迷惑行为",
            "default_topic": "季节·夏天·怕热日常"
        },
        "假期摆烂": {
            "sub_topic": "放假计划vs实际",
            "funny_example": "放假前计划 “学习/旅游”，实际躺平刷手机 7 天",
            "default_title": "假期摆烂天花板",
            "default_topic": "节日·假期·摆烂日常"
        }
    }
}

# 获取模板的快捷函数
def get_template(category, sub_category):
    """
    根据主分类+子分类获取模板信息
    :param category: 主分类（如"生活日常"）
    :param sub_category: 子分类（如"居家日常"）
    :return: 模板字典（title/topic/sub_topic/funny_example）
    """
    if category not in COMIC_TEMPLATES:
        return None
    if sub_category not in COMIC_TEMPLATES[category]:
        return None
    return COMIC_TEMPLATES[category][sub_category]

# 获取所有主分类
def get_all_categories():
    return list(COMIC_TEMPLATES.keys())

# 获取指定主分类下的所有子分类
def get_sub_categories(category):
    if category not in COMIC_TEMPLATES:
        return []
    return list(COMIC_TEMPLATES[category].keys())