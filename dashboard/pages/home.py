import streamlit as st


st.markdown(
    """
    <section class="volti-hero">
        <div class="volti-hero-content">
            <span class="volti-eyebrow">
                SMART ENERGY, MADE SIMPLE
            </span>

            <h1>
                Use energy when it costs less.
            </h1>

            <p>
                Volti turns your smart meter data into clear,
                personalised actions that help reduce your bill
                and carbon footprint.
            </p>

            <div class="volti-hero-actions">
                <a class="volti-primary-button" href="/Dashboard">
                    Open your dashboard
                </a>

                <a class="volti-secondary-button" href="/How_It_Works">
                    See how it works
                </a>
            </div>
        </div>

        <div class="volti-hero-visual">
            <div class="volti-saving-card">
                <span>Best action today</span>
                <strong>Run the dishwasher after 22:30</strong>
                <p>Estimated saving: £1.20</p>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <section class="volti-section">
        <div class="volti-section-heading">
            <span class="volti-eyebrow">WHY VOLTI?</span>
            <h2>Energy insights you can actually use</h2>
            <p>
                No complicated charts. No extra hardware.
                Just clear recommendations based on your usage.
            </p>
        </div>

        <div class="volti-feature-grid">
            <article class="volti-feature-card">
                <div class="volti-feature-icon">£</div>
                <h3>Save money</h3>
                <p>
                    Find cheaper times to run flexible appliances.
                </p>
            </article>

            <article class="volti-feature-card">
                <div class="volti-feature-icon">⚡</div>
                <h3>Take one clear action</h3>
                <p>
                    See what to change, when to change it,
                    and how much you could save.
                </p>
            </article>

            <article class="volti-feature-card">
                <div class="volti-feature-icon">CO₂</div>
                <h3>Use greener energy</h3>
                <p>
                    Shift consumption towards cleaner,
                    lower-demand periods.
                </p>
            </article>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <section class="volti-trust-section">
        <div>
            <span class="volti-eyebrow">BUILT AROUND YOU</span>
            <h2>Your energy data, without the complexity</h2>
        </div>

        <div class="volti-trust-points">
            <p>✓ Works without an EV, battery or extra hardware</p>
            <p>✓ Clear recommendations instead of raw data</p>
            <p>✓ Designed with privacy and transparency in mind</p>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)