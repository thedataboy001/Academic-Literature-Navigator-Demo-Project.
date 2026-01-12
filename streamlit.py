import streamlit as st
import requests

API_BASE_URL = "http://127.0.0.1:8000"

def literature_navigator():
    st.title("📚 Academic Literature Navigator")

    # init session state
    st.session_state.setdefault("document_id", None)
    st.session_state.setdefault("num_chunks", None)

    # -------------------------
    # PDF Upload
    # -------------------------
    st.header("Upload a Research Paper (PDF)")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        accept_multiple_files=False,
    )

    col1, col2 = st.columns([1, 1])
    process_clicked = col1.button("Process PDF", disabled=(uploaded_file is None))
    reset_clicked = col2.button("Reset")

    if reset_clicked:
        st.session_state["document_id"] = None
        st.session_state["num_chunks"] = None
        st.success("Cleared current paper. Upload a new one.")

    if uploaded_file and process_clicked:
        with st.spinner("Parsing and indexing paper..."):
            try:
                pdf_bytes = uploaded_file.getvalue()
                files = {"file": (uploaded_file.name, pdf_bytes, "application/pdf")}
                response = requests.post(f"{API_BASE_URL}/upload_pdf", files=files, timeout=180)
                response.raise_for_status()

                data = response.json()
                st.session_state["document_id"] = data["document_id"]
                st.session_state["num_chunks"] = data["num_chunks"]

                st.success(f"PDF processed successfully! ({data['num_chunks']} chunks)")
            except requests.HTTPError:
                try:
                    st.error(response.json())
                except Exception:
                    st.error(response.text)
            except requests.RequestException as e:
                st.error(f"Request failed: {e}")

    # -------------------------
    # Question Answering
    # -------------------------
    st.divider()

    if st.session_state["document_id"]:
        st.header("Ask a Question")
        st.caption(
            f"Active document_id: {st.session_state['document_id']} | "
            f"chunks: {st.session_state['num_chunks']}"
        )

        question = st.text_area(
            "Enter your question about the paper",
            placeholder="What is the main contribution of this paper?",
        )

        k = st.number_input("k", min_value=1, max_value=50, value=8, step=1)
        fetch_k = st.number_input("fetch_k", min_value=1, max_value=200, value=20, step=1)

        ask_clicked = st.button("Ask", disabled=(not question.strip()))

        if ask_clicked:
            with st.spinner("Searching paper and generating answer..."):
                try:
                    payload = {
                        "document_id": st.session_state["document_id"],
                        "question": question.strip(),
                        "k": int(k),
                        "fetch_k": int(fetch_k),
                    }
                    response = requests.post(f"{API_BASE_URL}/ask", json=payload, timeout=240)
                    response.raise_for_status()

                    answer = response.json().get("answer", "")
                    st.markdown("### ✅ Answer")
                    st.write(answer)

                except requests.HTTPError:
                    try:
                        st.error(response.json())
                    except Exception:
                        st.error(response.text)
                except requests.RequestException as e:
                    st.error(f"Request failed: {e}")
    else:
        st.info("Upload and process a PDF first, then you can ask questions.")

if __name__ == "__main__":
    literature_navigator()
