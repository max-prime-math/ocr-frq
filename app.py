"""
app.py — Streamlit web interface for PDF figure pre-extraction before MathPix.

Run with:
    streamlit run app.py
"""

import json
import logging
import os
import sys
import tempfile
from pathlib import Path

import streamlit as st
from anthropic import Anthropic

sys.path.insert(0, str(Path(__file__).parent / "src"))

from cache import FRQCache
from pdf_figure_extractor import preprocess_pdf_figures

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(
    page_title="PDF Figure Extraction",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📊 PDF Figure Pre-Extraction")
st.markdown("Extract vector figures from Manitoba Pre-Calculus 40S exam PDFs before MathPix OCR")


def init_session_state():
    """Initialize session state variables."""
    if "processing" not in st.session_state:
        st.session_state.processing = False
    if "manifest" not in st.session_state:
        st.session_state.manifest = None
    if "figure_paths" not in st.session_state:
        st.session_state.figure_paths = []
    if "output_pdf_path" not in st.session_state:
        st.session_state.output_pdf_path = None


def get_anthropic_client():
    """Get Anthropic client from user input or environment variable.

    Returns tuple of (client, is_valid).
    The API key is never stored or logged for security.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()

    return api_key


def main():
    """Main Streamlit app."""
    init_session_state()

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        st.markdown("---")

        st.subheader("🔑 Anthropic API Key")
        api_key_input = st.text_input(
            "Enter your API key",
            type="password",
            key="api_key_input",
            help="Your API key is not saved. It's only used for this session.",
        )

        # Try to use input key, fall back to env var
        api_key = api_key_input or os.environ.get("ANTHROPIC_API_KEY", "")

        if api_key:
            st.success("✓ API key configured")
            api_key_valid = True
        else:
            st.warning("⚠️ No API key provided. Enter your key to enable processing.")
            api_key_valid = False

        st.markdown("---")

        use_cache = st.checkbox("Use cache for Claude responses", value=True)
        dpi = st.slider("Figure extraction DPI", min_value=100, max_value=300, value=200, step=50)

        st.markdown("---")
        st.markdown("**About**")
        st.markdown(
            """
This app extracts vector figures from Manitoba Pre-Calculus 40S exam PDFs
before sending them to MathPix. Figures are replaced with `[figure ID]`
placeholders so MathPix can cleanly OCR the text and math.

**Output files:**
- Modified PDF with figures replaced
- PNG images of extracted figures
- JSON manifest mapping IDs to images
            """
        )

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📄 Upload PDF")
        uploaded_file = st.file_uploader(
            "Select an aggressive-cleaned PDF",
            type=["pdf"],
            help="Use PDFs ending in '_mg-only_cleaned_aggressive.pdf'",
        )

    with col2:
        st.subheader("📊 Stats")
        if st.session_state.manifest:
            num_figures = len(st.session_state.manifest.get("figures", []))
            st.metric("Figures Extracted", num_figures)

    if uploaded_file and api_key_valid:
        st.markdown("---")

        # Create temp directory for processing
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # Save uploaded file
            input_pdf = tmpdir / uploaded_file.name
            with open(input_pdf, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.info(f"📥 Uploaded: {uploaded_file.name} ({uploaded_file.size / 1024 / 1024:.1f} MB)")

            # Output paths
            output_pdf = tmpdir / input_pdf.name.replace(".pdf", "_nofigs.pdf")
            figures_dir = tmpdir / "figures"
            manifest_path = tmpdir / "manifest.json"

            if st.button("🚀 Extract Figures", disabled=st.session_state.processing):
                st.session_state.processing = True

                try:
                    progress_container = st.container()
                    with progress_container:
                        progress_bar = st.progress(0, text="Initializing...")

                        logger.info(f"Starting figure extraction on {input_pdf.name}")

                        # Initialize Claude client and cache with provided API key
                        client = Anthropic(api_key=api_key)
                        cache = FRQCache() if use_cache else None

                        progress_bar.progress(10, text="Analyzing PDF structure...")

                        # Run extraction
                        manifest = preprocess_pdf_figures(
                            input_pdf=str(input_pdf),
                            output_pdf=str(output_pdf),
                            figures_dir=str(figures_dir),
                            manifest_path=str(manifest_path),
                            claude_client=client,
                            cache=cache,
                            dpi=dpi,
                        )

                        progress_bar.progress(90, text="Finalizing...")

                        # Store results in session state
                        st.session_state.manifest = manifest
                        st.session_state.output_pdf_path = str(output_pdf)
                        st.session_state.figure_paths = list(figures_dir.glob("*.png"))

                        progress_bar.progress(100, text="✅ Complete!")

                        logger.info(
                            f"Extraction complete: {len(manifest['figures'])} figures extracted"
                        )

                except Exception as e:
                    st.error(f"❌ Error during extraction: {e}")
                    logger.exception("Extraction failed")

                finally:
                    st.session_state.processing = False

            # Display results
            if st.session_state.manifest:
                st.markdown("---")
                st.subheader("✅ Extraction Complete")

                manifest = st.session_state.manifest
                num_figures = len(manifest.get("figures", []))

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Figures Extracted", num_figures)
                with col2:
                    st.metric("Session", manifest.get("session_stem", "—"))
                with col3:
                    st.metric("Source PDF", Path(manifest.get("source_pdf", "")).stem)

                # Figures gallery
                if st.session_state.figure_paths:
                    st.markdown("### 🖼️ Extracted Figures")

                    cols_per_row = 3
                    for i in range(0, len(st.session_state.figure_paths), cols_per_row):
                        cols = st.columns(cols_per_row)
                        for j, col in enumerate(cols):
                            if i + j < len(st.session_state.figure_paths):
                                fig_path = st.session_state.figure_paths[i + j]
                                with col:
                                    st.image(str(fig_path), use_column_width=True)
                                    st.caption(fig_path.name)

                # Manifest display
                st.markdown("### 📋 Manifest")
                with st.expander("View figure manifest JSON"):
                    st.json(manifest)

                # Download buttons
                st.markdown("---")
                st.subheader("💾 Download Results")

                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.session_state.output_pdf_path and Path(st.session_state.output_pdf_path).exists():
                        with open(st.session_state.output_pdf_path, "rb") as f:
                            st.download_button(
                                label="📄 Download Modified PDF",
                                data=f.read(),
                                file_name=Path(st.session_state.output_pdf_path).name,
                                mime="application/pdf",
                            )

                with col2:
                    # Create zip of figures
                    if st.session_state.figure_paths:
                        import zipfile
                        import io

                        zip_buffer = io.BytesIO()
                        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                            for fig_path in st.session_state.figure_paths:
                                zf.write(fig_path, arcname=fig_path.name)

                        st.download_button(
                            label="🖼️ Download Figures (ZIP)",
                            data=zip_buffer.getvalue(),
                            file_name=f"{manifest.get('session_stem', 'figures')}_figures.zip",
                            mime="application/zip",
                        )

                with col3:
                    # Download manifest
                    st.download_button(
                        label="📋 Download Manifest",
                        data=json.dumps(manifest, indent=2),
                        file_name=f"{manifest.get('session_stem', 'manifest')}_figure_manifest.json",
                        mime="application/json",
                    )

    else:
        if not uploaded_file:
            st.info("👆 Upload a PDF to get started")


if __name__ == "__main__":
    main()
