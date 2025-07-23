FROM openjdk:17-jdk-slim

WORKDIR /leetcode_compiler

RUN useradd -ms /bin/bash executor && \
    mkdir -p /leetcode_compiler && \
    chown executor:executor /leetcode_compiler

# Install additional tools if needed
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy necessary files with correct ownership
COPY --chown=executor:executor compile_and_run.sh /bin/compile_and_run.sh
COPY --chown=executor:executor java.policy /leetcode_compiler/java.policy

RUN chmod +x /bin/compile_and_run.sh

# Verify files are in place
RUN ls -la /bin/compile_and_run.sh
RUN ls -la /leetcode_compiler/

USER executor

# Keep container running
CMD ["tail", "-f", "/dev/null"]
