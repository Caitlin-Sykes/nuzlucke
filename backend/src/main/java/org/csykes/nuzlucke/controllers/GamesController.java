package org.csykes.nuzlucke.controllers;

import lombok.extern.log4j.Log4j2;
import org.csykes.nuzlucke.criteria.GameSearchCriteria;
import org.csykes.nuzlucke.dto.GamesDto;
import org.csykes.nuzlucke.entity.GamesEntity;
import org.csykes.nuzlucke.mapper.GamesMapper;
import org.csykes.nuzlucke.repository.GamesRepository;
import org.csykes.nuzlucke.specifications.GamesSpecifications;
import org.springdoc.core.annotations.ParameterObject;
import org.springframework.data.domain.Sort;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/games")
@Log4j2
public class GamesController {

    private final GamesRepository gamesRepository;

    public GamesController(GamesRepository gamesRepository) {
        this.gamesRepository = gamesRepository;
    }

    /**
     * Retrieves a list of available games for the user to choose from.
     * Returns games sorted by id.
     * @param filter - criteria for filtering games, if not provided, returns all non-DLC games
     */
    @GetMapping("/available")
    public List<GamesDto> getAvailableGames(@ParameterObject GameSearchCriteria filter) {
        log.debug(">> getAvailableGames");
        Sort sort = Sort.sort(GamesEntity.class).by(GamesEntity::getId).ascending();

        // If the filter is null, return games that are not DLCs
        Specification<GamesEntity> spec = GamesSpecifications.build(filter);
        log.debug(spec);
        
        log.debug("<< getAvailableGames");
        try {
            return gamesRepository.findAll(spec, sort).stream()
                    .map(GamesMapper::toDto)
                    .toList(); 
        } catch (Exception e) {
            log.error("Error retrieving available games: {}", e.getMessage());
            throw e;
        }
        
       
        
    }
}
