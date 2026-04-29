package org.csykes.nuzlucke.converter;

import jakarta.persistence.AttributeConverter;
import jakarta.persistence.Converter;
import tools.jackson.databind.json.JsonMapper;

import java.util.LinkedHashMap;
import java.util.Map;

@Converter
/**
 * TODO: Remove this when Spring Boot 4 supports Hibernate 7.
 * Converter for mapping JSON maps to and from database columns.
 * This is needed until Spring 4, Jackson 3, and Hibernate 7 all have
 * compatible support for JSONB columns (and Jackson 3).
 */
public class JsonMapConverter implements AttributeConverter<Map<String, Object>, String> {

    private static final JsonMapper MAPPER = JsonMapper.builder().build();

    @Override
    public String convertToDatabaseColumn(Map<String, Object> attribute) {
        if (attribute == null) {
            return null;
        }
        try {
            return MAPPER.writeValueAsString(attribute);
        } catch (Exception ex) {
            throw new IllegalArgumentException("Unable to serialize JSON map", ex);
        }
    }

    @Override
    public Map<String, Object> convertToEntityAttribute(String dbData) {
        if (dbData == null || dbData.isBlank()) {
            return null;
        }
        try {
            return MAPPER.readValue(dbData, LinkedHashMap.class);
        } catch (Exception ex) {
            throw new IllegalArgumentException("Unable to deserialize JSON map", ex);
        }
    }
}
