"""
Model Handler Module.
This module is responsible for managing AI model interactions and API calls.
"""

import os
import json
import time
import threading
from typing import Dict, Any, Optional, List, Union
from enum import Enum

from kivy.logger import Logger


class ModelType(Enum):
    """Enum for supported AI model types."""
    CHATGPT = "chatgpt"
    GEMMA = "gemma"
    QISKIT = "qiskit"


class ModelHandler:
    """Handles interactions with various AI models."""
    
    def __init__(self):
        """Initialize the model handler."""
        self.models = {
            ModelType.CHATGPT: {"initialized": False, "api_key": None},
            ModelType.GEMMA: {"initialized": False, "api_key": None, "local_path": None},
            ModelType.QISKIT: {"initialized": False, "api_key": None}
        }
        
        # Threading lock for model initialization
        self.lock = threading.Lock()
    
    def initialize_openai(self, api_key: str) -> bool:
        """
        Initialize the OpenAI API.
        
        Args:
            api_key (str): OpenAI API key
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Import openai here to prevent immediate dependency requirement
            import openai
            from openai import OpenAI
            
            # Set API key
            client = OpenAI(api_key=api_key)
            
            # Test API connection
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello, are you working?"}],
                max_tokens=10
            )
            
            # Check if response is valid
            if response and hasattr(response, 'choices') and len(response.choices) > 0:
                # Store API key and client
                with self.lock:
                    self.models[ModelType.CHATGPT] = {
                        "initialized": True,
                        "api_key": api_key,
                        "client": client
                    }
                return True
            else:
                Logger.error("ModelHandler: OpenAI API initialization failed - invalid response")
                return False
                
        except Exception as e:
            Logger.error(f"ModelHandler: OpenAI API initialization failed: {e}")
            return False
    
    def initialize_gemma(self, api_key: Optional[str] = None, local_path: Optional[str] = None) -> bool:
        """
        Initialize the Gemma model.
        
        Args:
            api_key (str, optional): Gemma API key for cloud usage
            local_path (str, optional): Path to local Gemma model files
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not api_key and not local_path:
                Logger.error("ModelHandler: Either API key or local_path must be provided for Gemma")
                return False
            
            if local_path:
                # Try to initialize local Gemma model
                # This is a placeholder - in a real app, you'd use the actual Gemma SDK
                if os.path.exists(local_path):
                    with self.lock:
                        self.models[ModelType.GEMMA] = {
                            "initialized": True,
                            "api_key": None,
                            "local_path": local_path,
                            "mode": "local"
                        }
                    return True
                else:
                    Logger.error(f"ModelHandler: Local Gemma model not found at {local_path}")
                    return False
            else:
                # Initialize cloud Gemma API
                # This is a placeholder - in a real app, you'd use the actual Gemma API
                with self.lock:
                    self.models[ModelType.GEMMA] = {
                        "initialized": True,
                        "api_key": api_key,
                        "local_path": None,
                        "mode": "cloud"
                    }
                return True
                
        except Exception as e:
            Logger.error(f"ModelHandler: Gemma initialization failed: {e}")
            return False
    
    def initialize_qiskit(self, api_key: str) -> bool:
        """
        Initialize the Qiskit Runtime.
        
        Args:
            api_key (str): Qiskit API key
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # This is a placeholder - in a real app, you'd use the actual Qiskit SDK
            # Import qiskit here to prevent immediate dependency requirement
            # import qiskit
            
            with self.lock:
                self.models[ModelType.QISKIT] = {
                    "initialized": True,
                    "api_key": api_key
                }
            return True
                
        except Exception as e:
            Logger.error(f"ModelHandler: Qiskit initialization failed: {e}")
            return False
    
    def is_initialized(self, model_type: ModelType) -> bool:
        """
        Check if a specific model is initialized.
        
        Args:
            model_type (ModelType): The model type to check
            
        Returns:
            bool: True if initialized, False otherwise
        """
        return self.models.get(model_type, {}).get("initialized", False)
    
    def get_initialized_models(self) -> List[ModelType]:
        """
        Get a list of all initialized models.
        
        Returns:
            List[ModelType]: List of initialized model types
        """
        return [model_type for model_type in self.models if self.is_initialized(model_type)]
    
    def generate_text(self, model_type: ModelType, prompt: str) -> Dict[str, Any]:
        """
        Generate text using a specific model.
        
        Args:
            model_type (ModelType): The model to use
            prompt (str): Text prompt to send to the model
            
        Returns:
            Dict[str, Any]: Results dict with 'success', 'text', and optional 'error'
        """
        if not self.is_initialized(model_type):
            return {
                "success": False,
                "error": f"Model {model_type.value} is not initialized"
            }
        
        try:
            if model_type == ModelType.CHATGPT:
                return self._generate_chatgpt(prompt)
            elif model_type == ModelType.GEMMA:
                return self._generate_gemma(prompt)
            else:
                return {
                    "success": False,
                    "error": f"Text generation not supported for {model_type.value}"
                }
        except Exception as e:
            Logger.error(f"ModelHandler: Text generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_chatgpt(self, prompt: str) -> Dict[str, Any]:
        """
        Generate text using OpenAI's ChatGPT.
        
        Args:
            prompt (str): Text prompt to send to the model
            
        Returns:
            Dict[str, Any]: Results dict with 'success', 'text', and optional 'error'
        """
        try:
            model_info = self.models[ModelType.CHATGPT]
            client = model_info.get("client")
            
            if not client:
                return {"success": False, "error": "OpenAI client not initialized"}
            
            # Call the API
            response = client.chat.completions.create(
                model="gpt-4o",  # the newest OpenAI model is "gpt-4o" which was released May 13, 2024
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024
            )
            
            # Extract the generated text
            if response and hasattr(response, 'choices') and len(response.choices) > 0:
                generated_text = response.choices[0].message.content
                return {
                    "success": True,
                    "text": generated_text
                }
            else:
                return {
                    "success": False,
                    "error": "Invalid response from OpenAI API"
                }
                
        except Exception as e:
            Logger.error(f"ModelHandler: ChatGPT generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_gemma(self, prompt: str) -> Dict[str, Any]:
        """
        Generate text using Gemma.
        
        Args:
            prompt (str): Text prompt to send to the model
            
        Returns:
            Dict[str, Any]: Results dict with 'success', 'text', and optional 'error'
        """
        try:
            model_info = self.models[ModelType.GEMMA]
            mode = model_info.get("mode")
            
            if mode == "local":
                # This is a placeholder for local Gemma model inference
                # In a real app, you'd use the actual Gemma local inference
                local_path = model_info.get("local_path")
                
                # Simulate generation with a placeholder
                generated_text = f"[Local Gemma model response to: {prompt[:50]}...]"
                return {
                    "success": True,
                    "text": generated_text
                }
                
            elif mode == "cloud":
                # This is a placeholder for cloud Gemma API
                # In a real app, you'd use the actual Gemma cloud API
                api_key = model_info.get("api_key")
                
                # Simulate generation with a placeholder
                generated_text = f"[Cloud Gemma API response to: {prompt[:50]}...]"
                return {
                    "success": True,
                    "text": generated_text
                }
                
            else:
                return {
                    "success": False,
                    "error": "Invalid Gemma mode"
                }
                
        except Exception as e:
            Logger.error(f"ModelHandler: Gemma generation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_model_status(self, model_type: ModelType) -> Dict[str, Any]:
        """
        Get the status and info about a specific model.
        
        Args:
            model_type (ModelType): The model type to check
            
        Returns:
            Dict[str, Any]: Model status information
        """
        model_info = self.models.get(model_type, {})
        
        # Copy the dict to avoid exposing internal state
        status = model_info.copy()
        
        # Remove sensitive information
        if "api_key" in status:
            status["api_key"] = "***" if status["api_key"] else None
        
        # Remove internal objects
        if "client" in status:
            status["client"] = "initialized" if status["client"] else None
            
        return status