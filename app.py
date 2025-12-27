import streamlit as st
from openai import OpenAI

# ==========================================
# 1. 页面配置 (门面)
# ==========================================
st.set_page_config(page_title="爆款文案生成器", page_icon="✍️")
st.title("🚀 AI 爆款文案助手")
st.markdown("一人公司 MVP - 001号作品")

# ==========================================
# 2. 侧边栏 (配置区)
# ==========================================
with st.sidebar:
    st.header("⚙️ 设置")
    # 实际开发时，最好从环境变量读取 Key
    api_key = st.text_input("请输入 OpenAI/DeepSeek API Key", type="password")
    style = st.selectbox("选择风格", ["小红书种草风", "知乎硬核风", "朋友圈微商风"])

# ==========================================
# 3. 主界面 (交互区)
# ==========================================
product_desc = st.text_area("请输入你的产品/主题描述", height=150, placeholder="例如：一款C++程序员专用的机械键盘，手感重，声音脆...")
generate_btn = st.button("✨ 开始魔法生成")

# ==========================================
# 4. Agent 核心逻辑 (C++ 映射: 处理函数)
# ==========================================
def run_agent(desc, style_choice, key):
    if not key:
        return "❌ 请先在左侧输入 API Key"
    
    # 初始化客户端
    client = OpenAI(api_key=key, base_url="https://api.deepseek.com") # 举例用 DeepSeek，便宜

    # Prompt Engineering (核心资产)
    prompt = f"""
    你是一个资深的文案专家。请把以下产品描述改写成【{style_choice}】。
    
    产品描述：{desc}
    
    要求：
    1. 加入适当的 Emoji。
    2. 分段清晰。
    3. 语气要极其符合该平台的调性。
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-chat", # 或者 gpt-3.5-turbo
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"系统报错: {str(e)}"

# ==========================================
# 5. 执行与渲染
# ==========================================
if generate_btn:
    if not product_desc:
        st.warning("请先输入描述！")
    else:
        with st.spinner("Agent 正在疯狂思考中..."):
            result = run_agent(product_desc, style, api_key)
            st.success("生成完毕！")
            st.markdown("---")
            st.markdown(result)