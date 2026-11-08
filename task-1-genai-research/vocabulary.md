## Core model concepts

### Language model
A program that predicts text. You give it some words and it guesses what comes
next, one piece at a time, based on patterns it picked up from a huge amount of
text during training. 

### Token
The unit a model actually works with. Text is cut into tokens before the model
reads it, and limit counter in tokens

### Context window
The maximum amount of text a model can hold at once, counted in tokens. It
covers everything: your question, any documents you attach, and the answer being
written. 

### Inference
Running a trained model to get an answer. So inference happens everytime we ask llm about something.

### Prompt
The input you give the model. 

### Hallucination
When a model states something false with complete confidence. In code this shows
up as invented functions, parameters, or libraries that do not exist. The
dangerous part is not that it is wrong but that wrong output looks exactly like
correct output — there is no signal telling you when to doubt it.

---

## Retrieval and grounding

### RAG (Retrieval-Augmented Generation)
The method, which allows AI to look up relevant external documents first, then pass it to the
model before answering the question. 

### Chunking
Splitting a long document into smaller pieces before storing it. You need this
because a model can only read so much at once, and because a whole document is
too broad to match one specific question.

### Embedding
Text converted into a list of numbers that represents its meaning. So, getting the answer for question gets by comparing embedded values. 

### Vector database
Storage built for one specific job: given an embedding, find the stored items
closest to it, fast. An ordinary database searches for exact matches. A vector
database searches by similarity.

### Grounding
Making the model answer from sources you supply rather than from memory. A
grounded answer can point at the document it came from, which means a reader can
check it.

### Bottleneck
The narrowest part of a system, which limits everything else no matter how good
the other parts are. In RAG it is usually retrieval, not the model. 

---

### Agent
A model that takes multi-step actions instead of replying once. It can plan first, what to do next, act, look at the result, and try again. 


## Visual generation

### Diffusion model
The architecture behind image generators. During training it learns to reverse
the addition of random noise to images. To generate, it starts from pure noise
and removes it step by step, guided at each step by the text prompt, until a
coherent image appears.

### Temporal consistency
In video, the requirement that each frame is credible on its own and fits its
previous and future frames. For exmaple, objects keeping their shape, lighting staying stable, motion looking continuous. It is the main reason video generation is much
harder and more expensive than single images.

### Seed
The random starting value a generation begins from. The same prompt with the same
seed produces the same image, which is how you reproduce a result or make small
changes to one you already like instead of relying on random generation.

---

## Verbs

**to ground** — to make an answer rest on supplied sources rather than the
model's memory. *"The response is grounded in the retrieved policy documents."*

**to chunk** — to split a document into smaller passages for indexing.

**to fine-tune** — to train an existing model further on your own data so it
adapts to a specific domain or style.

**to prompt** — to give a model input intended to produce a particular kind of
output. 

**to infer** — to run the model and get output. 

**to retrieve** — to search and fetch the most relevant information to a question before answering.

