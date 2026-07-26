import streamlit as st


st.html(
    """
    <section class="page-hero">
        <div>
            <span class="volti-eyebrow">ABOUT VOLTI</span>
            <h1>Making smarter energy choices easier</h1>
            <p>
                Volti is an energy-coaching platform designed to help
                households understand their electricity use and take
                simple, practical steps towards lower bills.
            </p>
        </div>
    </section>
    """)


st.html(
    """
    <section class="about-grid">

        <article class="about-card about-card-primary">
            <span class="volti-eyebrow">OUR MISSION</span>
            <h2>Turn energy data into useful action</h2>
            <p>
                Smart meters generate valuable information, but raw
                consumption graphs rarely explain what someone should
                do next. Volti bridges that gap with clear and
                personalised recommendations.
            </p>
        </article>

        <article class="about-card">
            <span class="volti-eyebrow">WHO IT IS FOR</span>
            <h2>Built for real households</h2>
            <p>
                Volti is designed primarily for busy households that
                want to reduce energy costs without spending hours
                analysing tariffs, charts or technical data.
            </p>
        </article>

    </section>
    """
)


st.html(
    """
    <section class="volti-section">
        <div class="volti-section-heading">
            <span class="volti-eyebrow">OUR PRINCIPLES</span>
            <h2>Simple, transparent and action-focused</h2>
        </div>

        <div class="volti-feature-grid">

            <article class="volti-feature-card">
                <div class="volti-feature-icon">✓</div>
                <h3>Clarity first</h3>
                <p>
                    Recommendations are written in clear language,
                    with the most important action shown first.
                </p>
            </article>

            <article class="volti-feature-card">
                <div class="volti-feature-icon">🔒</div>
                <h3>Privacy conscious</h3>
                <p>
                    Energy information should be handled transparently
                    and only used to provide relevant insights.
                </p>
            </article>

            <article class="volti-feature-card">
                <div class="volti-feature-icon">🌱</div>
                <h3>Cost and carbon</h3>
                <p>
                    Volti presents financial and environmental impact
                    together, helping users make balanced decisions.
                </p>
            </article>

        </div>
    </section>
    """)


st.html(
    """
    <section class="about-cta">
        <span class="volti-eyebrow">START EXPLORING</span>
        <h2>Discover what your energy data can tell you</h2>
        <p>
            Open the dashboard to explore consumption, forecasts,
            potential anomalies and personalised recommendations.
        </p>
        <a class="volti-primary-button" href="/Dashboard">
            Open dashboard
        </a>
    </section>
    """)