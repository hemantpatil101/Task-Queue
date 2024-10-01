## Distributed Task Queue

- **Engineered a distributed task queue system** leveraging the Pub/Sub model with Flask and Redis. Tasks are enqueued and stored in Redis, then processed asynchronously by Celery workers for parallel execution, improving task throughput and scalability.
  
- **Optimized performance** through Redis caching, where task results are stored to prevent redundant computations and accelerate response times for frequently repeated tasks.

- **Implemented real-time status updates** using Server-Sent Events (SSE) over persistent HTTP connections, enabling smooth client-server communication for live task progress tracking.
