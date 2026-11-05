# Retiring the old queue

We moved the last consumer off the old queue in March, eight months after the first one. The move was
slow on purpose. Each consumer moved alone, ran for a week on the new queue, and only then did the
next one start. A queue carries other people's work, and a lost message is somebody's lost order.

The plan had three parts. First, every producer wrote to both queues. Second, each consumer moved to
the new queue and was watched for a week. Third, once nothing read the old queue, the producers
stopped writing to it. The first part took a day. The second took most of the eight months, because
each consumer had an owner, and each owner had other work.

The hardest consumer was the billing job. It read a message, charged a card, and then acknowledged the
message. If it crashed between the charge and the acknowledgement, the old queue delivered the message
again, and the card was charged twice. The old queue's retry delay was long enough that this almost
never happened. The new queue retried in seconds, and in the first test it happen four times in an
hour.

The fix was to make the charge safe to repeat. The job now sends an idempotency key with every charge,
built from the message id, and the payment provider refuses a second charge with the same key. With
that in place the retry delay stopped mattering, which is how it should have been from the start. A
consumer that is only correct because retries are slow is not correct.

```python
def charge(message):
    key = f"charge-{message.id}"
    provider.charge(message.card, message.amount, idempotency_key=key)
    message.ack()
```

Watching each consumer for a week sounds cautious, and it was. But a week covers a weekly batch, a
weekend's low traffic, and at least one deploy of the consumer itself. Two consumers failed in their
week, both in ways that a day would not have shown. One broke on the Sunday batch, and the other broke
when its owner deployed an unrelated change that held a connection open.

The week also gave each owner time to read the new queue's dashboards before they needed them. Most
had never looked at queue depth or consumer lag, because the old queue had no way to show either. By
the end of their week, each owner knew what normal looked like for their consumer, which made the
first real alert much easier to read.

Turning off the old queue was the quietest part. We stopped the producers writing to it, waited a
week for anything we had missed, and saw nothing arrive. Then we deleted it. Nobody noticed, which
was the point of the whole plan.

If I did it again I would move the consumers in order of risk, the riskiest first, while the team
still had the patience for it. We did them in order of ease, and the billing job came last, when
everyone was tired of the migration and wanted it finished. That is the wrong time to meet the
hardest problem.

I would also write the plan down before starting. Ours lived in a chat thread for the first two months,
and two consumers moved without anyone watching them, because nobody had said that watching was part
of the plan. Both were fine. We were lucky, and luck is not a plan anyone should be glad to rely on.
