# Validating Conditional Complex JSON Payload Using Marshmallow

It's very easy to validate incoming JSON payload using **Marshmallow** (a Python library to validate schema). But, what 
if the payload gets much more complicated? Let's consider the following scenario:

Suppose you have several repositories for your project. If repo `A` produces any error then send to repo `B` the error 
information along with the actual payload sent to repo `A` so that reo `B` can save the error details. Following are 
the possible errors:
