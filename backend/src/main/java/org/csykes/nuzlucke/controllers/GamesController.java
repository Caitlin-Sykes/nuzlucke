package org.csykes.nuzlucke.controllers;

import org.csykes.nuzlucke.dto.GamesDto;
import org.csykes.nuzlucke.repository.GamesRepository;
import org.springframework.data.domain.Sort;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/games")
public class GamesController {

    private final GamesRepository gamesRepository;

    public GamesController(GamesRepository gamesRepository) {
        this.gamesRepository = gamesRepository;
    }

    /**
     * Retrieves a list of available games for the user to choose from.
     * Returns games sorted by earliest release date.
     */
    @GetMapping("/available")
    public List<GamesDto> getAvailableGames() {
        return gamesRepository.findByIsDlcFalseOrIsDlcIsNull(Sort.by(Sort.Direction.ASC, "releaseDateUs")).stream()
                .map(GamesDto::fromEntity)
                .toList();
    }

    
}
