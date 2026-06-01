package org.csykes.nuzlucke.repository;

import org.csykes.nuzlucke.entity.GamesEntity;
import org.springframework.data.domain.Sort;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;

import java.util.List;

/**
 * Repository for {@link GamesEntity}.
 */
public interface GamesRepository extends JpaRepository<GamesEntity, Integer>, JpaSpecificationExecutor<GamesEntity> {

    /**
     * Finds all games that are not DLC.
     * @param sort - Sorting criteria.
     * @return List of games that are not DLC.
     */
    @EntityGraph(attributePaths = {"region", "metadata"})
    List<GamesEntity> findByIsDlcFalseOrIsDlcIsNull(Sort sort);
}
