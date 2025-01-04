import React from 'react';
import styled from 'styled-components';

const Loader = () => {
    return (
      <StyledWrapper>
        <div className="spinner">
          <div className="spinner1" />
        </div>
      </StyledWrapper>
    );
  }
  
  const StyledWrapper = styled.div`
    .spinner {
      background-image: linear-gradient(rgb(186, 66, 255) 35%,rgb(0, 225, 255));
      width: 50px;
      height: 50px;
      animation: spinning82341 1.7s linear infinite, hue 1s ease-in-out infinite;
      text-align: center;
      border-radius: 50px;
      filter: blur(1px);
      box-shadow: 0px -5px 20px 0px rgb(186, 66, 255), 0px 5px 20px 0px rgb(0, 225, 255);
    }
  
    .spinner1 {
      background-color: rgb(36, 36, 36);
      width: 50px;
      height: 50px;
      border-radius: 50px;
      filter: blur(10px);
    }
  
    @keyframes spinning82341 {
      to {
        transform: rotate(360deg);
      }
    }
  
    @keyframes hue {
      0% {
        filter: hue-rotate(0deg);
      }
  
      100% {
        filter: hue-rotate(360deg);
      }
    }`;
  
  export default Loader;
  