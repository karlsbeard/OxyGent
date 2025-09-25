---
title: "Reflexion Flow"
description: "Iterative self-improvement flow that refines answers through reflection and feedback"
---

# Reflexion Flow

The Reflexion flow implements an iterative self-improvement methodology that enhances answer quality through systematic evaluation, reflection, and iterative refinement. This approach is particularly effective for complex problems requiring high-quality, well-reasoned responses.

## Overview

The Reflexion methodology follows a cyclical improvement process:

1. **Generation**: Worker agent produces an initial response
2. **Evaluation**: Reflexion agent evaluates response quality
3. **Reflection**: System analyzes evaluation feedback
4. **Improvement**: Worker agent refines the response based on feedback
5. **Iteration**: Process repeats until satisfactory quality is achieved

This approach significantly improves output quality by incorporating self-criticism and iterative refinement, leading to more accurate, complete, and well-structured responses.

## Class Hierarchy

```python
from oxygent.oxy.flows import Reflexion, MathReflexion
```

### Inheritance Structure

```
BaseFlow
└── Reflexion
    └── MathReflexion
```

## Core Classes

### Reflexion

The base reflexion flow for general-purpose iterative improvement.

#### Key Attributes

**Agent Configuration:**
- **`worker_agent`** (`str`): Agent that generates and refines responses
  - Default: `"worker_agent"`
  - Role: Primary response generation and improvement

- **`reflexion_agent`** (`str`): Agent that evaluates response quality
  - Default: `"reflexion_agent"`
  - Role: Quality assessment and improvement suggestions

**Flow Control:**
- **`max_reflexion_rounds`** (`int`): Maximum number of improvement iterations
  - Default: `3`
  - Prevents infinite refinement loops

**Response Processing:**
- **`func_parse_worker_response`** (`Optional[Callable]`): Custom worker response parser
- **`func_parse_reflexion_response`** (`Optional[Callable]`): Custom evaluation parser
- **`pydantic_parser_reflexion`** (`PydanticOutputParser`): Structured evaluation parser

**Templates:**
- **`evaluation_template`** (`str`): Template for quality evaluation queries
- **`improvement_template`** (`str`): Template for improvement instructions

### MathReflexion

Specialized reflexion flow optimized for mathematical problems and calculations.

#### Specialized Features

- **Pre-configured Agents**: Uses `math_expert_agent` and `math_checker_agent`
- **Math-Specific Evaluation**: Focuses on calculation accuracy and mathematical reasoning
- **Step-by-Step Validation**: Checks mathematical procedures and formulas
- **Specialized Templates**: Math-focused evaluation criteria

## Data Models

### ReflectionEvaluation

```python
class ReflectionEvaluation(BaseModel):
    """Reflection evaluation result."""
    
    is_satisfactory: bool = Field(
        description="Whether the answer is satisfactory"
    )
    evaluation_reason: str = Field(
        description="Detailed explanation of the evaluation"
    )
    improvement_suggestions: str = Field(
        default="", 
        description="Specific improvement suggestions if unsatisfactory"
    )
```

## Usage Examples

### Basic Reflexion Flow

```python
from oxygent.oxy.flows import Reflexion

# Create general reflexion flow
reflexion_flow = Reflexion(
    name="quality_improver",
    desc="Iterative quality improvement through reflexion",
    worker_agent="content_generator",
    reflexion_agent="quality_evaluator", 
    max_reflexion_rounds=5
)

# Execute with reflexion
request = OxyRequest(
    callee="quality_improver",
    arguments={
        "query": "Explain the benefits and challenges of renewable energy adoption"
    }
)

response = await request.call()
# Response includes iteratively improved answer
```

### Mathematical Problem Solving

```python
from oxygent.oxy.flows import MathReflexion

# Create specialized math reflexion flow
math_flow = MathReflexion(
    name="math_solver", 
    desc="Mathematical problem solver with verification",
    max_reflexion_rounds=4
)

# Solve complex math problem
request = OxyRequest(
    callee="math_solver",
    arguments={
        "query": "Find the derivative of f(x) = x^3 * ln(x) + 2x^2 - 5x + 1"
    }
)

response = await request.call()
# Response includes verified mathematical solution
```

### Custom Evaluation Criteria

```python
# Create reflexion flow with custom evaluation template
detailed_flow = Reflexion(
    name="detailed_evaluator",
    desc="Comprehensive answer evaluation and improvement",
    worker_agent="expert_writer",
    reflexion_agent="critical_reviewer",
    max_reflexion_rounds=6,
    
    evaluation_template="""Evaluate this response comprehensively:

Question: {query}
Answer: {answer}

Evaluation Criteria:
1. Technical Accuracy (1-10): Factual correctness and precision
2. Completeness (1-10): Coverage of all relevant aspects  
3. Clarity (1-10): Clear structure and easy comprehension
4. Practical Value (1-10): Actionable insights and usefulness
5. Professional Quality (1-10): Language quality and tone

Overall Assessment:
- Strengths: What works well in this response?
- Weaknesses: What needs improvement?  
- Missing Elements: What important aspects are missing?

Provide detailed feedback with specific, actionable improvement suggestions.

Format your response as:
- is_satisfactory: true/false (true only if all scores are 8+)
- evaluation_reason: [Detailed analysis with scores]
- improvement_suggestions: [Specific actionable improvements]""",
    
    improvement_template="""{original_query}

Your previous response needs improvement. Please provide a better answer based on this detailed feedback:

{improvement_suggestions}

Previous response: {previous_answer}

Focus on addressing the specific weaknesses identified and enhancing the overall quality, accuracy, and usefulness of your response."""
)
```

### Domain-Specific Reflexion

```python
class TechnicalReflexion(Reflexion):
    """Reflexion flow optimized for technical documentation."""
    
    def __init__(self, **kwargs):
        # Set technical writing defaults
        kwargs.setdefault("worker_agent", "technical_writer")
        kwargs.setdefault("reflexion_agent", "technical_reviewer")
        kwargs.setdefault("max_reflexion_rounds", 4)
        
        # Technical evaluation template
        kwargs.setdefault("evaluation_template", """
        Evaluate this technical response for:

        Question: {query}
        Answer: {answer}

        Technical Writing Criteria:
        1. Accuracy: Are technical details correct?
        2. Completeness: Are all necessary steps/concepts covered?
        3. Clarity: Is it understandable for the target audience?
        4. Structure: Is information well-organized?
        5. Examples: Are there sufficient practical examples?
        6. Best Practices: Does it follow industry standards?

        Assessment:
        - is_satisfactory: true/false
        - evaluation_reason: [Technical assessment]
        - improvement_suggestions: [Specific technical improvements]
        """)
        
        super().__init__(**kwargs)

# Usage
tech_flow = TechnicalReflexion(
    name="technical_documenter",
    desc="Technical documentation with expert review"
)
```

## Advanced Usage Patterns

### Multi-Agent Reflexion

```python
class MultiAgentReflexion(Reflexion):
    """Reflexion with multiple evaluators."""
    
    def __init__(self, evaluator_agents=None, **kwargs):
        super().__init__(**kwargs)
        self.evaluator_agents = evaluator_agents or [
            "accuracy_evaluator",
            "clarity_evaluator", 
            "completeness_evaluator"
        ]
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute with multi-agent evaluation."""
        
        original_query = oxy_request.get_query()
        current_query = original_query
        
        for round_num in range(self.max_reflexion_rounds + 1):
            # Get worker response
            worker_response = await oxy_request.call(
                callee=self.worker_agent,
                arguments={"query": current_query}
            )
            
            current_answer = worker_response.output
            
            # Multi-agent evaluation
            evaluations = []
            for evaluator in self.evaluator_agents:
                eval_query = self.evaluation_template.format(
                    query=original_query, 
                    answer=current_answer
                )
                
                eval_response = await oxy_request.call(
                    callee=evaluator,
                    arguments={"query": eval_query}
                )
                
                evaluations.append({
                    "evaluator": evaluator,
                    "assessment": eval_response.output
                })
            
            # Aggregate evaluations
            aggregated_evaluation = self._aggregate_evaluations(evaluations)
            
            if aggregated_evaluation.is_satisfactory:
                return OxyResponse(
                    state=OxyState.COMPLETED,
                    output=f"Multi-agent verified answer (Round {round_num + 1}):\n\n{current_answer}",
                    extra={
                        "reflexion_rounds": round_num + 1,
                        "evaluations": evaluations,
                        "aggregated_evaluation": aggregated_evaluation.dict()
                    }
                )
            
            # Prepare improvement query
            if round_num < self.max_reflexion_rounds:
                current_query = self.improvement_template.format(
                    original_query=original_query,
                    improvement_suggestions=aggregated_evaluation.improvement_suggestions,
                    previous_answer=current_answer
                )
        
        # Return final attempt
        return OxyResponse(
            state=OxyState.COMPLETED,
            output=f"Final answer after {self.max_reflexion_rounds + 1} rounds:\n\n{current_answer}",
            extra={
                "reflexion_rounds": self.max_reflexion_rounds + 1,
                "reached_max_rounds": True,
                "evaluations": evaluations
            }
        )
    
    def _aggregate_evaluations(self, evaluations):
        """Aggregate multiple evaluations into single assessment."""
        
        # Count satisfactory evaluations
        satisfactory_count = sum(
            1 for eval in evaluations 
            if "satisfactory" in eval["assessment"].lower()
        )
        
        # Require majority satisfaction
        is_satisfactory = satisfactory_count >= len(evaluations) / 2
        
        # Combine improvement suggestions
        suggestions = []
        for eval in evaluations:
            # Extract suggestions from each evaluation
            suggestions.append(f"[{eval['evaluator']}]: {eval['assessment']}")
        
        return ReflectionEvaluation(
            is_satisfactory=is_satisfactory,
            evaluation_reason=f"Multi-agent evaluation: {satisfactory_count}/{len(evaluations)} satisfactory",
            improvement_suggestions="\n".join(suggestions)
        )
```

### Progressive Quality Enhancement

```python
class ProgressiveReflexion(Reflexion):
    """Reflexion with progressive quality targets."""
    
    def __init__(self, quality_thresholds=None, **kwargs):
        super().__init__(**kwargs)
        self.quality_thresholds = quality_thresholds or [6, 7, 8, 9]  # Progressive targets
        self.current_threshold_index = 0
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute with progressive quality enhancement."""
        
        original_query = oxy_request.get_query()
        quality_history = []
        
        for round_num in range(self.max_reflexion_rounds + 1):
            # Current quality target
            target_quality = self.quality_thresholds[
                min(self.current_threshold_index, len(self.quality_thresholds) - 1)
            ]
            
            # Enhanced evaluation template with quality target
            enhanced_template = f"""
            {self.evaluation_template}
            
            QUALITY TARGET: This response must score at least {target_quality}/10 overall.
            
            Rate the response and determine if it meets the quality target of {target_quality}/10.
            """
            
            # Execute round with quality target
            worker_response = await oxy_request.call(
                callee=self.worker_agent,
                arguments={"query": original_query if round_num == 0 else current_query}
            )
            
            current_answer = worker_response.output
            
            # Evaluate with quality target
            eval_query = enhanced_template.format(
                query=original_query,
                answer=current_answer
            )
            
            eval_response = await oxy_request.call(
                callee=self.reflexion_agent,
                arguments={"query": eval_query}
            )
            
            evaluation = self.func_parse_reflexion_response(eval_response.output)
            
            # Track quality progress
            quality_history.append({
                "round": round_num + 1,
                "target_quality": target_quality,
                "evaluation": evaluation.dict(),
                "answer_length": len(current_answer)
            })
            
            # Check if target quality is met
            if evaluation.is_satisfactory:
                # Advance to next quality threshold
                self.current_threshold_index += 1
                
                # If we've reached the highest threshold, we're done
                if self.current_threshold_index >= len(self.quality_thresholds):
                    return OxyResponse(
                        state=OxyState.COMPLETED,
                        output=f"High-quality answer achieved (Target: {target_quality}/10):\n\n{current_answer}",
                        extra={
                            "reflexion_rounds": round_num + 1,
                            "quality_history": quality_history,
                            "final_quality_target": target_quality
                        }
                    )
            
            # Prepare improvement query if not at max rounds
            if round_num < self.max_reflexion_rounds:
                current_query = self.improvement_template.format(
                    original_query=original_query,
                    improvement_suggestions=f"Target Quality: {target_quality}/10\n{evaluation.improvement_suggestions}",
                    previous_answer=current_answer
                )
        
        # Return best attempt
        return OxyResponse(
            state=OxyState.COMPLETED,
            output=f"Best answer after progressive enhancement:\n\n{current_answer}",
            extra={
                "reflexion_rounds": self.max_reflexion_rounds + 1,
                "quality_history": quality_history,
                "reached_max_rounds": True
            }
        )
```

### Specialized Use Cases

```python
# Code Review Reflexion
class CodeReflexion(Reflexion):
    """Specialized reflexion for code review and improvement."""
    
    def __init__(self, **kwargs):
        kwargs.setdefault("worker_agent", "code_generator")
        kwargs.setdefault("reflexion_agent", "code_reviewer")
        
        kwargs.setdefault("evaluation_template", """
        Review this code solution:

        Problem: {query}
        Code: {answer}

        Code Review Checklist:
        1. Correctness: Does the code solve the problem correctly?
        2. Efficiency: Is the algorithm/approach optimal?
        3. Readability: Is the code clean and well-documented?
        4. Best Practices: Does it follow language conventions?
        5. Error Handling: Are edge cases properly handled?
        6. Testing: Are there adequate test cases?

        Format:
        - is_satisfactory: true/false
        - evaluation_reason: [Detailed code review]
        - improvement_suggestions: [Specific code improvements]
        """)
        
        super().__init__(**kwargs)

# Creative Writing Reflexion
class CreativeReflexion(Reflexion):
    """Specialized reflexion for creative content."""
    
    def __init__(self, **kwargs):
        kwargs.setdefault("worker_agent", "creative_writer")
        kwargs.setdefault("reflexion_agent", "creative_critic")
        
        kwargs.setdefault("evaluation_template", """
        Evaluate this creative response:

        Prompt: {query}
        Response: {answer}

        Creative Evaluation:
        1. Originality: Is it creative and unique?
        2. Engagement: Is it compelling and interesting?
        3. Coherence: Does it flow well and make sense?
        4. Style: Is the writing style appropriate?
        5. Emotional Impact: Does it evoke appropriate emotions?
        6. Completeness: Does it fully address the prompt?

        Assessment:
        - is_satisfactory: true/false
        - evaluation_reason: [Creative assessment]
        - improvement_suggestions: [Creative enhancement suggestions]
        """)
        
        super().__init__(**kwargs)
```

## Integration with OxyGent Framework

### In OxySpace Configuration

```python
def create_reflexion_flows():
    """Create various reflexion flows for different use cases."""
    
    return [
        # General purpose reflexion
        Reflexion(
            name="general_reflexion",
            desc="General purpose quality improvement through reflexion",
            worker_agent="general_worker",
            reflexion_agent="quality_evaluator",
            max_reflexion_rounds=4
        ),
        
        # Mathematical reflexion
        MathReflexion(
            name="math_reflexion", 
            desc="Mathematical problem solving with verification",
            max_reflexion_rounds=5
        ),
        
        # High-quality content generation
        Reflexion(
            name="premium_content",
            desc="Premium quality content with rigorous evaluation",
            worker_agent="expert_writer",
            reflexion_agent="senior_editor",
            max_reflexion_rounds=6,
            evaluation_template="""..."""  # Custom high-standard template
        ),
        
        # Technical documentation
        TechnicalReflexion(
            name="technical_docs",
            desc="Technical documentation with expert review"
        ),
        
        # Code review system
        CodeReflexion(
            name="code_improver",
            desc="Code generation and improvement through review"
        )
    ]
```

### Custom Workflow Integration

```python
from oxygent.oxy.flows import Workflow, Reflexion

async def hybrid_reflexion_workflow(oxy_request: OxyRequest):
    """Combine reflexion with custom pre/post processing."""
    
    # Pre-processing
    enhanced_query = preprocess_query(oxy_request.get_query())
    
    enhanced_request = OxyRequest(
        callee=oxy_request.callee,
        arguments={"query": enhanced_query}
    )
    
    # Use reflexion for core processing
    reflexion_flow = Reflexion(
        worker_agent="specialized_agent",
        reflexion_agent="domain_expert",
        max_reflexion_rounds=4
    )
    
    reflexion_result = await reflexion_flow._execute(enhanced_request)
    
    # Post-processing
    final_output = postprocess_result(reflexion_result.output)
    
    return {
        "original_query": oxy_request.get_query(),
        "enhanced_query": enhanced_query,
        "reflexion_result": reflexion_result.output,
        "final_output": final_output,
        "processing_metadata": reflexion_result.extra
    }

# Create hybrid workflow
hybrid_flow = Workflow(
    name="enhanced_reflexion",
    desc="Reflexion with custom pre/post processing",
    func_workflow=hybrid_reflexion_workflow
)
```

## Best Practices

### 1. Agent Selection and Specialization

```python
# Use complementary agents for better reflexion
quality_flow = Reflexion(
    name="high_quality_generator",
    
    # Generator focused on comprehensive responses  
    worker_agent="comprehensive_writer",
    
    # Evaluator focused on critical analysis
    reflexion_agent="critical_analyst",
    
    max_reflexion_rounds=5
)
```

### 2. Evaluation Template Design

```python
# Design specific, actionable evaluation criteria
specific_template = """
Evaluate this response systematically:

Question: {query}
Answer: {answer}

Specific Evaluation Criteria:
1. Factual Accuracy (1-10): Check all factual claims
2. Logical Structure (1-10): Assess argument flow and organization
3. Completeness (1-10): Identify missing important aspects
4. Clarity (1-10): Evaluate readability and comprehension
5. Practical Value (1-10): Assess actionability and usefulness

For each criterion scoring below 8:
- Identify specific problems
- Provide concrete improvement suggestions
- Reference examples or best practices

Required format:
- is_satisfactory: true (only if ALL criteria score 8+)
- evaluation_reason: [Score breakdown with specific issues]
- improvement_suggestions: [Prioritized, actionable improvements]
"""
```

### 3. Performance Optimization

```python
class OptimizedReflexion(Reflexion):
    """Performance-optimized reflexion flow."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Cache for similar evaluations
        self.evaluation_cache = {}
        
        # Early stopping criteria
        self.early_stop_threshold = 0.95  # Stop if very high quality
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute with performance optimizations."""
        
        # Check cache for similar queries
        query_hash = hash(oxy_request.get_query())
        if query_hash in self.evaluation_cache:
            cached_result = self.evaluation_cache[query_hash]
            if self._is_cache_valid(cached_result):
                return self._adapt_cached_result(cached_result, oxy_request)
        
        # Execute with early stopping
        result = await self._execute_with_early_stopping(oxy_request)
        
        # Cache successful results
        if result.state == OxyState.COMPLETED:
            self.evaluation_cache[query_hash] = result
        
        return result
    
    async def _execute_with_early_stopping(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute with early stopping for high-quality responses."""
        
        for round_num in range(self.max_reflexion_rounds + 1):
            # Standard reflexion round
            worker_response = await oxy_request.call(
                callee=self.worker_agent,
                arguments={"query": oxy_request.get_query()}
            )
            
            # Quick quality check for early stopping
            quality_score = self._quick_quality_assessment(worker_response.output)
            
            if quality_score >= self.early_stop_threshold:
                return OxyResponse(
                    state=OxyState.COMPLETED,
                    output=f"High-quality answer (early stop at round {round_num + 1}):\n\n{worker_response.output}",
                    extra={
                        "reflexion_rounds": round_num + 1,
                        "early_stopped": True,
                        "quality_score": quality_score
                    }
                )
            
            # Continue with standard reflexion logic...
            # (Implementation continues)
```

### 4. Error Handling and Fallbacks

```python
class RobustReflexion(Reflexion):
    """Reflexion with robust error handling."""
    
    async def _execute(self, oxy_request: OxyRequest) -> OxyResponse:
        """Execute with comprehensive error handling."""
        
        try:
            return await super()._execute(oxy_request)
            
        except Exception as e:
            logger.error(f"Reflexion execution failed: {str(e)}")
            
            # Fallback to simple generation
            return await self._fallback_execution(oxy_request)
    
    async def _fallback_execution(self, oxy_request: OxyRequest) -> OxyResponse:
        """Fallback to simple worker execution."""
        
        try:
            # Simple worker execution without reflexion
            fallback_response = await oxy_request.call(
                callee=self.worker_agent,
                arguments={"query": oxy_request.get_query()}
            )
            
            return OxyResponse(
                state=OxyState.COMPLETED,
                output=f"Response (reflexion fallback): {fallback_response.output}",
                extra={"fallback_used": True}
            )
            
        except Exception as fallback_error:
            logger.error(f"Fallback also failed: {str(fallback_error)}")
            
            # Ultimate fallback
            return OxyResponse(
                state=OxyState.FAILED,
                output="Unable to generate response due to system errors"
            )
```

## Common Use Cases

1. **Content Quality Assurance**: Improve articles, reports, and documentation
2. **Code Review and Enhancement**: Iteratively improve code quality
3. **Academic Writing**: Enhance research papers and academic content
4. **Mathematical Problem Solving**: Verify and improve mathematical solutions
5. **Creative Content**: Refine stories, marketing copy, and creative writing
6. **Technical Documentation**: Ensure accuracy and completeness
7. **Decision Analysis**: Improve decision-making through critical evaluation
8. **Educational Content**: Create high-quality teaching materials

## Performance Considerations

- **Iteration Overhead**: Multiple rounds increase latency but improve quality
- **Agent Selection Impact**: Specialized agents provide better results but may be slower
- **Template Complexity**: Detailed evaluation templates improve quality but increase processing time
- **Early Stopping Benefits**: Can significantly reduce processing time for high-quality initial responses
- **Caching Opportunities**: Similar queries can benefit from cached evaluations

## Technical Notes

- Reflexion rounds are counted from 1 (first attempt) to max_reflexion_rounds + 1
- Each round builds on feedback from the previous evaluation
- The flow automatically handles parser fallbacks if Pydantic parsing fails
- Evaluation results are included in the response extra data
- MathReflexion inherits all Reflexion capabilities with math-specific defaults
- Custom parsers can be provided for specialized evaluation formats

## Related Documentation

- [BaseFlow](/base-flow) - Base class for all flows
- [Workflow](/workflow-flow) - Custom workflow execution
- [ParallelFlow](/parallel-flow) - Concurrent execution flow
- [PlanAndSolve](/plan-and-solve-flow) - Planning and execution flow
- [PydanticOutputParser](/pydantic-parser) - Structured output parsing
- [OxyRequest](/oxy-request) - Request object structure
- [OxyResponse](/oxy-response) - Response object structure