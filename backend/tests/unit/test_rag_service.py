from app.services.rag_service import chunk_text


def test_chunk_text():
    # Arrange
    text = (
        "This is the first paragraph of the news article. It discusses the recent earnings report of Apple. "
        "The report states that revenues are up by 10% year over year.\n\n"
        "This is the second paragraph. It talks about the new product launches and how they might affect future sales. "
        "Investors are very optimistic about the upcoming quarter."
    )
    
    # Act
    chunks = chunk_text(text)
    
    # Assert
    assert len(chunks) > 0, "Should generate at least one chunk"
    # Ensure it doesn't just chunk arbitrarily by character without respecting spaces/newlines
    for chunk in chunks:
        assert len(chunk) <= 500, "Chunks should be smaller than or equal to the max chunk size"
