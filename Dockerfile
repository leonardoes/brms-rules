FROM adoptopenjdk/openjdk8:x86_64-alpine-jdk8u292-b10-slim as builder
ARG JAR_FILE=*.jar
COPY ${JAR_FILE} application.jar
COPY config/ config/
FROM adoptopenjdk/openjdk8:x86_64-alpine-jdk8u292-b10-slim
RUN mkdir ./app
COPY --from=builder application.jar ./app
COPY --from=builder config/ ./app/config
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "application.jar"]