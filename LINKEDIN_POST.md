Safe to Send · Ep 20 — Old runbooks never die

A short one, with a lesson I learned the hard way.

I asked a simple search over four runbooks: "how do I pause a delivery that is already sending?"

It returned the 2021 runbook first. The one that says "if the delivery does not pause, pause the MTA".

The current runbook says the opposite: never restart the MTA, it affects every market.

Why did the old one win? It says "pause" and "delivery" over and over. Old documents are often wordier, so they match keywords better.

The fix wasn't a better model. It was two fields of metadata: "supersedes" and "review by". Superseded runbooks drop out, and anything past review gets a warning.

Retrieval quality is a document-hygiene problem before it's an AI problem.

Repo: https://github.com/sghatge/safe-to-send-20-fresh-search

#SafeToSend #RAG #KnowledgeManagement
