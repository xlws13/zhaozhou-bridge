import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import font_manager
import os

# 设置中文字体 (确保系统中有中文字体，此处使用常见字体回退)
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 页面配置
st.set_page_config(
    page_title="赵州桥·天下第一桥",
    page_icon="🌉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------
# 样式美化
# ------------------------------
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        color: #8B4513;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size: 1.3rem;
        color: #5D4A3A;
        text-align: center;
        margin-bottom: 2rem;
        font-style: italic;
    }
    .card {
        background-color: #FDF8F5;
        border-left: 6px solid #B87333;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #A0522D;
    }
    .caption {
        color: #6E5C4B;
        font-size: 0.9rem;
    }
    .source-footer {
        background-color: #F0EDE9;
        padding: 1rem;
        border-radius: 8px;
        font-size: 0.8rem;
        color: #4A3B32;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------
# 数据定义 (来源于文档)
# ------------------------------
# 模块2：构件数量
component_data = pd.DataFrame({
    '构件': ['主拱拱券', '敞肩小拱', '栏板', '望柱', '拱脚条石层数'],
    '数量': [28, 4, 42, 40, 5],
    '作用': [
        '并列砌筑，独立支撑，冗余安全',
        '减重15%，提升泄洪抗震',
        '雕刻斗子卷叶/行龙，隋代原物存1/3',
        '栏板间装饰柱，雕刻精美',
        '平铺拱脚下，分散荷载增强稳定'
    ]
})

# 模块3：关键尺寸
dimension_data = pd.DataFrame({
    '指标': ['桥身全长', '主拱净跨径', '石拱高度', '拱顶宽度', '拱脚宽度'],
    '数值(米)': [64.4, 37.02, 7.23, 9.0, 9.6],
    '设计意义': [
        '单孔长跨，河心不立墩',
        '坦弧设计，跨度大坡度缓',
        '矢跨比≈1:5.25，适配石材受力',
        '桥面宽阔，满足古代交通',
        '拱脚加宽，分散水平推力'
    ]
})

# 模块4：受力对比
force_data = pd.DataFrame({
    '状态': ['有伏石+腰铁拉结', '无伏石拉结'],
    '竖向反力(kN)': [1146.6, 1408.0],
    '水平推力(kN)': [1345.6, 1442.5]
})

# 安全系数
safety_factor = 3.8

# 模块5：桥台基础
abutment_data = {
    '尺寸': '长约5米，宽9.6米，厚1.549米',
    '结构': '拱脚下5层平铺条石，灰缝薄无裂缝',
    '作用': '分散桥梁荷载，增强桥台稳定性'
}
foundation_data = {
    '尺寸': '宽9.6-10米，长约5.5米，埋深2-2.5米',
    '构造': '天然地基，承载力适配桥体',
    '成就': '1400余年无明显下沉或倾斜'
}

# 图片文件名 (请确保图片与脚本同目录，或修改路径)
IMG_3D = "zhaozq_3d.jpg"  # 赵州桥3D结构拆解
IMG_OPEN_SPANDREL = "zhaozq_cg.jpg"  # 敞肩拱结构示意图
IMG_DRAGON = "zhaozq_xy.jpg"  # 栏板雕刻·行龙纹样
IMG_SJ="zhaozq_quanj.jpg" #赵州桥实景 (示意)
IMG_QMKJ="zhaozq_qt.jpg" #桥台基础剖面示意图
# ------------------------------
# 侧边栏 - 概览与导航
# ------------------------------
with st.sidebar:
    if os.path.exists(IMG_SJ):
        st.image(IMG_SJ, use_container_width=True, caption="赵州桥实景 (示意)")
    else:
        st.warning(f"图片 `{IMG_SJ}` 未找到，请将图片置于当前目录。此处展示占位图。")
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Zhaozhou_Bridge.jpg/640px-Zhaozhou_Bridge.jpg",
             caption="赵州桥实景 (示意)", use_container_width=True)
    st.markdown("## 🏯 赵州桥 (安济桥)")
    st.markdown("**天下第一桥** · 隋 · 李春主持建造")
    st.markdown("---")
    st.markdown("### 📜 历史地位")
    st.success("世界现存最早、保存最完整的单孔敞肩石拱桥")
    st.markdown("**四大工艺成就**")
    st.markdown("- 敞肩拱\n- 坦弧大跨度\n- 腰铁固石\n- 纵向并列砌筑")
    st.markdown("---")
    st.markdown("### 🧭 快速导航")
    nav = st.radio(
        "跳转至模块",
        ["🏠 首页概览", "📊 构件数量", "📏 关键尺寸", "⚙️ 受力分析", "🧱 桥台基础", "🔨 建造工艺"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("### 📚 权威数据来源")
    st.caption(
        "罗英《中国古代桥梁史》《中国石桥》\n\n河北省赵县地方志《赵州桥志》\n\n梁思成《赵县大石桥》1934\n\n河北省文物局《维修勘察报告》1986\n\n清华&天大《受力分析报告》2012")

# ------------------------------
# 主内容区域
# ------------------------------
st.markdown('<div class="main-header">🌉 赵州桥 · 结构智慧与千年匠心</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">敞肩拱 · 坦弧 · 腰铁 · 并列砌筑 —— 隋代工匠李春的不朽杰作</div>',
            unsafe_allow_html=True)

# 根据侧边栏导航显示不同模块 (默认首页)
if nav.startswith("🏠"):
    # ---------- 模块1：首页概览 ----------
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### 🧱 3D结构拆解")
        if os.path.exists(IMG_3D):
            st.image(IMG_3D, use_container_width=True, caption="赵州桥3D结构拆解示意")
        else:
            st.warning(f"图片 `{IMG_3D}` 未找到，请将图片置于当前目录。此处展示占位图。")
            st.image("https://via.placeholder.com/600x400/8B4513/FFFFFF?text=Zhaozhou+Bridge+3D+Structure",
                     use_container_width=True)
    with col2:
        st.markdown("### 🏛️ 核心简介")
        st.markdown("""
        <div class="card">
        <p style="font-size:1.1rem;">隋代工匠<strong>李春</strong>主持建造，世界现存最早、保存最完整的单孔敞肩石拱桥。以<strong>敞肩拱、坦弧大跨度、腰铁固石、纵向并列砌筑</strong>四大工艺成就千年不朽，彰显中国古代工匠卓越智慧与匠心。</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("#### 👤 建造者")
        st.markdown("**李春** (隋代杰出工匠)")
        st.markdown("#### 🏆 历史地位")
        st.markdown("世界桥梁史上不朽丰碑，中国古代工匠智慧巅峰之作")
        st.markdown("#### ✨ 敞肩拱示意图")
        if os.path.exists(IMG_OPEN_SPANDREL):
            st.image(IMG_OPEN_SPANDREL, use_container_width=True, caption="敞肩拱结构示意")
        else:
            st.info(f"敞肩拱示意图 `{IMG_OPEN_SPANDREL}` 未找到")

    st.markdown("---")
    st.markdown("### 🖼️ 栏板雕刻 · 行龙纹样")
    col_img, col_txt = st.columns([2, 1])
    with col_img:
        if os.path.exists(IMG_DRAGON):
            st.image(IMG_DRAGON, use_container_width=True, caption="栏板行龙纹样 (隋代原物风格)")
        else:
            st.warning(f"图片 `{IMG_DRAGON}` 未找到")
    with col_txt:
        st.markdown("**栏板42块，望柱约40根**，雕刻斗子卷叶、行龙等精美纹饰，隋代原物尚存约1/3，是古代石雕艺术瑰宝。")
        st.markdown("> “龙兽之状，蟠绕拏踞，眭盱翕欻，若飞若动”—— 唐·张嘉贞《石桥铭序》")

elif nav.startswith("📊"):
    # ---------- 模块2：构件数量可视化 ----------
    st.markdown("## 📊 核心构件数量总览")
    st.markdown("数据来源：罗英《中国古代桥梁史》、梁思成《赵县大石桥》")

    col_chart, col_info = st.columns([3, 2])
    with col_chart:
        # 饼图 (Altair 交互)
        pie = alt.Chart(component_data).mark_arc().encode(
            theta=alt.Theta(field="数量", type="quantitative"),
            color=alt.Color(field="构件", type="nominal", legend=alt.Legend(title="构件类型")),
            tooltip=['构件', '数量', '作用']
        ).properties(width=400, height=400, title="构件数量占比")
        st.altair_chart(pie, use_container_width=True)

        # 柱状图
        bar = alt.Chart(component_data).mark_bar(color='#B87333').encode(
            x=alt.X('构件', sort='-y', title=None),
            y=alt.Y('数量', title='数量'),
            tooltip=['构件', '数量', '作用']
        ).properties(width=600, height=300, title="构件数量对比")
        st.altair_chart(bar, use_container_width=True)

    with col_info:
        st.markdown("### 🔍 构件详情")
        selected_comp = st.selectbox("点击选择构件查看详情", component_data['构件'].tolist())
        comp_row = component_data[component_data['构件'] == selected_comp].iloc[0]
        st.markdown(f"**{comp_row['构件']}**  \n数量: **{comp_row['数量']}**  \n作用: {comp_row['作用']}")
        st.markdown("---")
        st.markdown("**📌 补充数据**")
        st.markdown("- 主拱拱券: 28道，每道宽约35cm，含27道拱缝")
        st.markdown("- 勾石/腰铁: 数百件，横向拉结28道拱券")
        st.markdown("- 敞肩小拱: 主拱两端各2个，共4个")
        st.markdown("- 拱脚条石: 5层平铺")

    st.markdown("### 🗿 栏板雕刻艺术")
    if os.path.exists(IMG_DRAGON):
        st.image(IMG_DRAGON, width=500, caption="行龙纹样拓片/示意")

elif nav.startswith("📏"):
    # ---------- 模块3：关键尺寸可视化 ----------
    st.markdown("## 📏 关键结构尺寸 (实测精准值)")
    st.caption("数据来源：河北省文物局《安济桥维修工程勘察报告》1986")

    # 尺寸柱状图
    bar_dim = alt.Chart(dimension_data).mark_bar(color='#A0522D').encode(
        x=alt.X('指标', sort=dimension_data['指标'].tolist(), title=None),
        y=alt.Y('数值(米)', title='长度 (米)'),
        tooltip=['指标', '数值(米)', '设计意义']
    ).properties(width=700, height=350, title="主拱尺寸对比")
    st.altair_chart(bar_dim, use_container_width=True)

    st.markdown("### 📐 尺寸详情与设计智慧")
    cols = st.columns(len(dimension_data))
    for i, (idx, row) in enumerate(dimension_data.iterrows()):
        with cols[i]:
            st.markdown(f"<div style='background:#F9F3EE; padding:15px; border-radius:10px; height:180px;'>"
                        f"<h3 style='color:#8B4513;'>{row['数值(米)']} m</h3>"
                        f"<strong>{row['指标']}</strong><br>"
                        f"<small>{row['设计意义']}</small>"
                        f"</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**矢跨比 ≈ 1:5.25** —— 坦拱结构，拱内以轴向压力为主，弯矩极小，完美适配石材抗压特性。")

elif nav.startswith("⚙️"):
    # ---------- 模块4：28道拱券受力分析 ----------
    st.markdown("## ⚙️ 28道拱券受力机制与动态对比")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("### 🧩 结构特点")
        st.markdown("""
        - **28道独立拱券** 并列砌筑 (每道宽约35cm)
        - **收分结构**：拱石下宽上窄，自然向内挤压
        - **横向锁固**：勾石、腰铁、伏石防错位
        - **冗余安全**：单券损坏不影响整体
        """)
        st.markdown("### 💪 现代力学实测")
        st.metric(label="结构安全系数", value=f"{safety_factor}", delta="远超古代一般桥梁")
        st.caption("清华大学&天津大学联合研究报告，2012")

    with col2:
        st.markdown("### 🔀 切换拉结状态对比")
        state = st.radio("选择受力状态", force_data['状态'].tolist(), horizontal=True)
        selected = force_data[force_data['状态'] == state].iloc[0]
        st.markdown(f"**竖向反力**: {selected['竖向反力(kN)']} kN")
        st.markdown(f"**水平推力**: {selected['水平推力(kN)']} kN")

        # 绘制对比柱状图 (Matplotlib)
        fig, ax = plt.subplots(figsize=(6, 4))
        x = ['竖向反力', '水平推力']
        y_sel = [selected['竖向反力(kN)'], selected['水平推力(kN)']]
        bars = ax.bar(x, y_sel, color=['#D2B48C', '#CD853F'])
        ax.set_ylabel('力 (kN)')
        ax.set_title(f'{state}受力值')
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height + 20, f'{height:.1f}', ha='center', va='bottom')
        st.pyplot(fig)

        # 折线图对比 (Altair)
        force_melt = force_data.melt(id_vars=['状态'], var_name='受力类型', value_name='数值(kN)')
        line_chart = alt.Chart(force_melt).mark_line(point=True).encode(
            x='受力类型',
            y='数值(kN)',
            color='状态',
            tooltip=['状态', '受力类型', '数值(kN)']
        ).properties(width=500, height=300, title="有/无拉结受力对比折线图")
        st.altair_chart(line_chart, use_container_width=True)

    st.markdown("### 🎯 受力机制通俗解析")
    st.info("""
    **为什么这样设计更稳固？**  
    - **分散荷载**：28道拱券共同分担，局部损坏不致命。  
    - **坦拱纯压**：矢跨比小，拱内几乎无弯矩，石材抗压能力充分发挥。  
    - **敞肩减重**：4个小拱减重约700吨，主拱水平推力降低25%。  
    - **腰铁锁固**：铁水浇灌腰铁，将拱券横向拉结为整体，防止外倾。
    """)

elif nav.startswith("🧱"):
    # ---------- 模块5：桥台及基础结构 ----------
    st.markdown("## 🧱 桥台与基础 —— 千年稳固之基")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### 🪨 桥台结构")
        st.json(abutment_data)
        st.markdown("**拱脚下5层平铺条石**，灰缝极薄，下层石料稍厚，有效分散荷载。")
    with col_b:
        st.markdown("### ⛰️ 基础数据")
        st.json(foundation_data)
        st.success("**1400余年无明显下沉或倾斜** —— 古代地基工程的奇迹。")

    st.markdown("### 📍 剖面示意图 (点击模拟交互)")
    # 由于无法真实交互，采用expander模拟点击弹出详情
    with st.expander("🔽 点击查看桥台/基础剖面详解"):
        st.markdown(f"""
        **桥台尺寸**: {abutment_data['尺寸']}  
        **结构**: {abutment_data['结构']}  
        **作用**: {abutment_data['作用']}  

        **基础尺寸**: {foundation_data['尺寸']}  
        **构造**: {foundation_data['构造']}  
        **成就**: {foundation_data['成就']}
        """)
        if os.path.exists(IMG_QMKJ):
            st.image(IMG_QMKJ, use_container_width=True, caption="桥台基础剖面示意图")
        else:
            st.image("https://via.placeholder.com/600x300/BC8F8F/FFFFFF?text=桥台基础剖面示意图", use_container_width=True)

else:  # 建造工艺
    # ---------- 模块6：建造工艺与细节 ----------
    st.markdown("## 🔨 建造流程与工艺亮点")
    st.markdown("### 🛠️ 千年建造工序")
    steps = [
        "**1. 勘测选址**：实地勘察洨河水文地质，选定浅埋桥台桥址。",
        "**2. 石料加工**：开采花岗岩，精准打磨28道拱券石料，锻造腰铁。",
        "**3. 主拱砌筑**：纵向并列砌筑37.02米坦弧主拱。",
        "**4. 敞肩施工**：主拱两端砌筑4个小拱，首创敞肩拱结构。",
        "**5. 千年传承**：工艺留存，至今保存完整。"
    ]
    for step in steps:
        st.markdown(f"- {step}")

    st.markdown("---")
    st.markdown("### ✨ 工艺亮点")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**纵向并列砌筑**  \n模块化构造，便于维修且安全性高。")
    with col2:
        st.markdown("**腰铁固石**  \n铁水浇灌腰铁，拱石连接严丝合缝。")
    with col3:
        st.markdown("**敞肩拱设计**  \n世界首创，减重泄洪双效合一。")

    if os.path.exists(IMG_OPEN_SPANDREL):
        st.image(IMG_OPEN_SPANDREL, caption="敞肩拱结构示意图", use_container_width=True)
    else:
        st.info("敞肩拱示意图未找到，请确认图片。")

# ------------------------------
# 底部统一标注
# ------------------------------
st.markdown("---")
st.markdown("""
<div class="source-footer">
    <strong>📖 数据权威来源：</strong> 罗英《中国古代桥梁史》《中国石桥》 · 河北省赵县地方志《赵州桥志》 · 梁思成《中国营造学社汇刊·赵县大石桥》(1934) · 河北省文物局《安济桥维修工程勘察报告》(1986) · 清华大学&天津大学《赵州桥结构受力分析与稳定性评估》(2012) · 王其亨《中国古建筑力学》<br>
    <strong>🖱️ 交互说明：</strong> 所有数据均为实测/文献真实数据。图表支持悬停查看详情，点击构件下拉框查看详情。页面基于Streamlit构建，可自由切换模块。
</div>
""", unsafe_allow_html=True)