package org.csykes.nuzlucke.dto;

import java.time.LocalDate;

/**
 * DTO for game release dates.
 * @param releaseDateEu - European Release Date
 * @param releaseDateJp - Japanese Release Date
 * @param releaseDateAu - Australian Release Date
 * @param releaseDateUs - US Release Date
 */
public record ReleaseDatesDto(
        LocalDate releaseDateEu,
        LocalDate releaseDateJp,
        LocalDate releaseDateAu,
        LocalDate releaseDateUs
) {
}
