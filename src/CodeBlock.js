// CodeBlock Component: Displays the selected code block, handles role assignments, and facilitates real-time code updates using socket connections.

import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { io } from "socket.io-client";
import CodeMirror from "@uiw/react-codemirror";
import { javascript } from "@codemirror/lang-javascript";
import styled from "styled-components";

// Initialize the socket connection
const socket = io("http://127.0.0.1:5000");

const CodeBlock = () => {
  // Retrieve the code block ID from the URL parameters
  const { id } = useParams();

  // State variables
  const [code, setCode] = useState("");  // Code for the selected code block
  const [role, setRole] = useState(null);  // User role (mentor or student)
  const [smiley, setSmiley] = useState(false);  // Display smiley face after correct solution
  const [studentCount, setStudentCount] = useState(0);  // Track the number of students in the room
  const [blockTitle, setBlockTitle] = useState("");  // Store the title of the selected code block
  const navigate = useNavigate();  // Hook for navigation

  useEffect(() => {
    // Fetch the list of available code blocks and set the selected block's code and title
    fetch(`http://127.0.0.1:5000/codeblocks`)
      .then(response => response.json())
      .then(data => {
        const selectedBlock = data.find(block => block.id.toString() === id);
        if (selectedBlock) {
          setCode(selectedBlock.template);  // Set the initial code template
          setBlockTitle(selectedBlock.title);  // Set the title dynamically
        }
      })
      .catch(error => console.error("Error fetching code block:", error));

    // Emit a socket event to join the room for the specific code block
    socket.emit("join_codeblock", { id: Number(id), username: "Tom" });

    // Listen for updates to the code block templates
    socket.on("update_codeblocks", (updatedCodeBlocks) => {
      const updatedBlock = updatedCodeBlocks.find(block => block.id.toString() === id);
      if (updatedBlock) setCode(updatedBlock.template);
    });

    // Listen for role assignments (mentor or student)
    socket.on("role_assigned", (data) => {
      setRole(data.role);
    });

    // Listen for the event to display the smiley face for correct solution
    socket.on("show_smiley", () => {
      setSmiley(true);
      setTimeout(() => setSmiley(false), 3000);
    });

    // Listen for updates on student count in the room
    socket.on("student_count_update", (data) => {
      setStudentCount(data.count);
    });

    // Listen for the event to redirect to the lobby page
    socket.on("redirect_to_lobby", () => {
      navigate("/lobby");
    });

    // Cleanup event listeners on component unmount
    return () => {
      socket.off("update_codeblocks");
      socket.off("role_assigned");
      socket.off("show_smiley");
      socket.off("student_count_update");
      socket.off("redirect_to_lobby");
    };
  }, [id, navigate]);  // Re-run the effect when the code block ID or navigate changes

  return (
    <Container>
      <Header>
        <h2>{`Code Block: ${blockTitle}`}</h2>
        <p>{`Students in room: ${studentCount}`}</p>
      </Header>

      {role === "mentor" ? (
        <MentorWrapper>
          <p>You are the Mentor</p>
          <CodeMirrorWrapper>
            <CodeMirror value={code} readOnly extensions={[javascript()]} />
          </CodeMirrorWrapper>
        </MentorWrapper>
      ) : (
        <StudentWrapper>
          <p>You are a Student</p>
          <CodeMirrorWrapper>
            <CodeMirror
              value={code}
              extensions={[javascript()]}
              onChange={(value) => {
                setCode(value);
                socket.emit("update_codeblock", { id: Number(id), template: value });
              }}
            />
          </CodeMirrorWrapper>
        </StudentWrapper>
      )}

      {smiley && <Smiley>Great job! 🙂</Smiley>}
    </Container>
  );
};

export default CodeBlock;

// Styled components for the layout and design :)

const Container = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f4f8;
  font-family: 'Arial', sans-serif;
`;

const Header = styled.header`
  text-align: center;
  margin-bottom: 20px;

  h2 {
    font-size: 2rem;
    color: #333;
  }

  p {
    font-size: 1rem;
    color: #666;
  }
`;

const MentorWrapper = styled.div`
  background-color: #e0e7ff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 80%;
  max-width: 800px;
`;

const StudentWrapper = styled.div`
  background-color: #fef9c3;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 80%;
  max-width: 800px;
`;

const CodeMirrorWrapper = styled.div`
  margin-top: 20px;
  border-radius: 8px;
  overflow: hidden;
  background-color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
`;

const Smiley = styled.h1`
  font-size: 3rem;
  color: #ffcc00;
  animation: smileyAnim 1s ease-out infinite;

  @keyframes smileyAnim {
    0% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.2);
    }
    100% {
      transform: scale(1);
    }
  }
`;
