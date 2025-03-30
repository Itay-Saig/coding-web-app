// Lobby Component: Retrieves a list of code blocks from the server and allows the user
// to navigate to the corresponding code block when selected.

import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { io } from "socket.io-client";
import styled from "styled-components";

// Initialize socket connection to the server
const socket = io("http://127.0.0.1:5000");

const Lobby = () => {
  const [codeBlocks, setCodeBlocks] = useState([]);  // State to store code blocks fetched from the server
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch code blocks from the server when the component mounts
    fetch("http://127.0.0.1:5000/codeblocks")
      .then((response) => response.json())  // Parse the response as JSON
      .then((data) => setCodeBlocks(data))  // Set the retrieved code blocks in state
      .catch((error) => console.error("Error fetching code blocks:", error));

    // Cleanup socket connection on component unmount
    return () => {
      socket.disconnect();
    };
  }, []);  // The empty dependency array ensures this effect runs only once, when the component is mounted

  return (
    <Container>
      <Header>
        <Title>Choose a Code Block</Title>
      </Header>
      <CodeBlockList>
        {codeBlocks.map((block) => (
          <CodeBlockItem key={block.id}>
            <CodeBlockButton onClick={() => navigate(`/codeblock/${block.id}`)}>
              {block.title}
            </CodeBlockButton>
          </CodeBlockItem>
        ))}
      </CodeBlockList>
    </Container>
  );
};

export default Lobby;

// Styled components for the layout and design :)

const Container = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f4f7fa;
  font-family: 'Arial', sans-serif;
`;

const Header = styled.header`
  text-align: center;
  margin-bottom: 30px;
`;

const Title = styled.h1`
  font-size: 2.5rem;
  color: #333;
  font-weight: 600;
`;

const CodeBlockList = styled.ul`
  list-style: none;
  padding: 0;
  width: 80%;
  max-width: 600px;
`;

const CodeBlockItem = styled.li`
  margin: 10px 0;
`;

const CodeBlockButton = styled.button`
  width: 100%;
  padding: 15px;
  font-size: 1.2rem;
  font-weight: 500;
  color: white;
  background-color: #4caf50;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;

  &:hover {
    background-color: #45a049;
    transform: translateY(-2px);
  }

  &:active {
    background-color: #388e3c;
  }

  &:focus {
    outline: none;
  }
`;
