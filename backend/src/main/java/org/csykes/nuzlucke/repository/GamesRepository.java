package org.csykes.nuzlucke.repository;

import org.csykes.nuzlucke.entity.GamesEntity;
import org.springframework.data.domain.Sort;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.EntityGraph;

import java.util.List;

/**
 * Repository for {@link GamesEntity}.
 */
public interface GamesRepository extends JpaRepository<GamesEntity, Integer> {

    /**
     * Finds all games that are not DLC.
     * @param sort - Sorting criteria.
     * @return List of games that are not DLC.
     */
    @EntityGraph(attributePaths = {"region", "metadata"})
    List<GamesEntity> findByIsDlcFalseOrIsDlcIsNull(Sort sort);
}
