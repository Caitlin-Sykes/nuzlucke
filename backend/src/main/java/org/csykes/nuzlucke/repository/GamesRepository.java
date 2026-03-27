package org.csykes.nuzlucke.repository;

import org.csykes.nuzlucke.entity.GamesEntity;
import org.springframework.data.domain.Sort;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.EntityGraph;

import java.util.List;

public interface GamesRepository extends JpaRepository<GamesEntity, Integer> {

    @EntityGraph(attributePaths = "region")
    List<GamesEntity> findByIsDlcFalseOrIsDlcIsNull(Sort sort);

}
