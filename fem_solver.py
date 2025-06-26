import os
import logging
from typing import TypedDict, Generator, Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import START, StateGraph, END

class State(TypedDict):
    problem: str
    gemini_response: str
    openai_response: str
    Final_response: str

class FEMSolver:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key is required")
        
        # Set the API key in environment for langchain
        os.environ["GOOGLE_API_KEY"] = self.api_key
        
        self.setup_workflow()
    
    def setup_workflow(self):
        """Initialize the LangGraph workflow"""
        self.workflow = StateGraph(State)
        self.workflow.add_node("FemLLMSolver", self.fem_solver)
        self.workflow.add_edge(START, "FemLLMSolver")
        self.workflow.add_edge("FemLLMSolver", END)
        self.app = self.workflow.compile()
    
    def fem_solver(self, state: State) -> State:
        """Main FEM solver function using multiple models"""
        system_prompt = ChatPromptTemplate.from_template(
            "You are an expert Finite Element Analysis (FEA) engineer at the peak of your career, "
            "known for solving FEA problems with absolute precision and no errors. Your task is to "
            "carefully read and understand the finite element problem described below and solve it "
            "step-by-step, ensuring maximum accuracy at each stage. Provide clear reasoning, "
            "appropriate formulas, and accurate calculations. Finally, give the exact numerical "
            "answer to the question.\n\nProblem Description: {Description}"
        )
        
        # Initialize models
        llm1 = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=self.api_key)
        llm2 = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", google_api_key=self.api_key)
        
        # Create chains
        chain1 = system_prompt | llm1
        chain2 = system_prompt | llm2
        
        # Get responses from both models
        init_res1 = chain1.invoke({"Description": state["problem"]})
        init_res2 = chain2.invoke({"Description": state["problem"]})
        
        # Revision prompt for combining responses
        revision_prompt = ChatPromptTemplate.from_template(
            "You are given multiple numerical responses from different LLMs for a problem, "
            "where Result 2 is from the best reasoning model and should be given slightly more weight. "
            "Analyze all responses: if most values are closely clustered and one or more are "
            "significantly different, treat the outliers as noise and exclude them. Only consider "
            "values that are numerically close to each other, and compute the average of those. "
            "If multiple values are significantly different with no clear clustering, identify "
            "potential calculation errors and provide the most reasonable answer with detailed explanation.\n\n"
            "Result 1: {result1}\n\nResult 2: {result2}\n\n"
            "Provide the final consolidated answer with clear reasoning."
        )
        
        llm_final_thinker = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=self.api_key)
        chain_final_thinker = revision_prompt | llm_final_thinker
        init_combined_response = chain_final_thinker.invoke({
            "result1": init_res1.content,
            "result2": init_res2.content
        })
        
        return {
            "problem": state["problem"],
            "gemini_response": init_res1.content,
            "openai_response": init_res2.content,
            "Final_response": init_combined_response.content
        }
    
    def solve_streaming(self, problem: str) -> Generator[Dict[str, Any], None, None]:
        """Solve FEM problem with streaming updates"""
        try:
            yield {"type": "status", "message": "Initializing FEM solver..."}
            
            yield {"type": "status", "message": "Processing with Gemini 1.5-flash..."}
            
            # Run the workflow
            result = self.app.invoke({"problem": problem})
            
            yield {"type": "gemini_response", "content": result["gemini_response"]}
            
            yield {"type": "status", "message": "Processing with Gemini 2.0-flash..."}
            yield {"type": "openai_response", "content": result["openai_response"]}
            
            yield {"type": "status", "message": "Combining responses..."}
            yield {"type": "final_start", "message": "Generating final response..."}
            
            # Stream the final response word by word
            final_response = result["Final_response"]
            words = final_response.split()
            
            for i, word in enumerate(words):
                if i == 0:
                    yield {"type": "final_chunk", "content": word}
                else:
                    yield {"type": "final_chunk", "content": " " + word}
            
            yield {"type": "complete", "message": "Analysis complete"}
            
        except Exception as e:
            logging.error(f"Error in FEM solver: {str(e)}")
            yield {"type": "error", "message": f"Error: {str(e)}"}

# Template for multiple model support (commented out for now)
"""
class MultiModelFEMSolver:
    def __init__(self, api_keys: Dict[str, str]):
        self.api_keys = api_keys
        self.models = {}
        self.setup_models()
    
    def setup_models(self):
        # Setup Gemini models
        if "gemini" in self.api_keys:
            self.models["gemini-1.5-flash"] = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash", 
                google_api_key=self.api_keys["gemini"]
            )
            self.models["gemini-2.0-flash"] = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-exp", 
                google_api_key=self.api_keys["gemini"]
            )
        
        # Setup OpenAI models
        if "openai" in self.api_keys:
            from langchain_openai import ChatOpenAI
            self.models["gpt-4"] = ChatOpenAI(
                model="gpt-4",
                openai_api_key=self.api_keys["openai"]
            )
            self.models["gpt-3.5-turbo"] = ChatOpenAI(
                model="gpt-3.5-turbo",
                openai_api_key=self.api_keys["openai"]
            )
        
        # Setup Anthropic models
        if "anthropic" in self.api_keys:
            from langchain_anthropic import ChatAnthropic
            self.models["claude-3-sonnet"] = ChatAnthropic(
                model="claude-3-sonnet-20240229",
                anthropic_api_key=self.api_keys["anthropic"]
            )
    
    def solve_with_multiple_models(self, problem: str, selected_models: List[str]) -> Generator:
        for model_name in selected_models:
            if model_name in self.models:
                yield {"type": "model_start", "model": model_name}
                # Process with individual model
                # yield responses...
"""
