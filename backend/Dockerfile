FROM amazoncorretto:21.0.10-alpine AS build

#Sets the directory for docker to store stuff in
WORKDIR /backend

COPY pom.xml .
COPY src ./src
COPY .mvn/ ./.mvn
COPY mvnw pom.xml ./

# Build the jar
RUN ./mvnw clean package -DskipTests

FROM amazoncorretto:21.0.10-alpine
WORKDIR /backend
LABEL "author"="Cait"
LABEL "nuzlucke.backend.version"="1.0.0A"
LABEL "nuzlucke.release-date"="2026-02-18"
LABEL "description"="This is the backend for the Nuzlucke project. This is built using Java 21, and Spring Boot "

#Copy from the build stage 
COPY --from=build /backend/target/*.jar nuzlucke.jar

# Expose the spring boot port- in my case its on 8081 as per app.properties
EXPOSE 8081

#Run it
ENTRYPOINT ["java", "-jar", "nuzlucke.jar"]