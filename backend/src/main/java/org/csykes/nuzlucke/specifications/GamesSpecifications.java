package org.csykes.nuzlucke.specifications;

import jakarta.persistence.criteria.Join;
import lombok.extern.log4j.Log4j2;
import org.csykes.nuzlucke.criteria.GameSearchCriteria;
import org.csykes.nuzlucke.entity.GamesEntity;
import org.springframework.data.jpa.domain.Specification;
import java.util.function.Function;

/**
 * Specifications for {@link GamesEntity} queries.
 * This is useful for filtering and querying games based on various criteria.
 */
@Log4j2
public class GamesSpecifications {

    public static Specification<GamesEntity> build(GameSearchCriteria criteria) {
        // If criteria is null, return only non-DLC games
        if (criteria == null) {
            log.debug("<< build - criteria is null, returning non-DLC games");
            return Specification.where(isNotDlc());
        }
        return Specification.where(isNotDlc())
                .and(ifPresent(criteria.nameLike(), GamesSpecifications::nameLike))
                .and(ifPresent(criteria.gen(), GamesSpecifications::hasGeneration))
                .and(ifPresent(criteria.region(), GamesSpecifications::hasRegion));
    }
    
    /**
     * Returns results based on whether the name of the game is like the filter
     * @param name - The name to filter by, case-insensitive
     * @return filtered results
     */
    public static Specification<GamesEntity> nameLike(String name) {
        return (root, query, cb) -> {
            if (name == null || name.isBlank()) return null;
            return cb.like(cb.lower(root.get("name")), "%" + name.toLowerCase() + "%");
        };
    }

    /**
     * Returns results based on whether the region is similar to what is typed
     * @param regionName - The region to filter by, case-insensitive
     * @return filtered results
     */
    public static Specification<GamesEntity> hasRegion(String regionName) {
        return (root, query, cb) -> {
            if (regionName == null || regionName.isBlank()) return null;

            Join<Object, Object> regionJoin = root.join("region");

            return cb.like(
                    cb.lower(regionJoin.get("name")),
                    "%" + regionName.toLowerCase() + "%"
            );
        };
    }

    /**
     * Returns results based on whether the generation is similar to what is typed
     * @param gen - The generation to filter by
     * @return filtered results
     */
    public static Specification<GamesEntity> hasGeneration(int gen) {
        return (root, query, cb) -> cb.equal(root.get("rulesetId"), gen);
    }

    /**
     * Returns results that are not DLCs
     * @return filtered results
     */
    public static Specification<GamesEntity> isNotDlc() {
        return (root, query, cb) ->
                cb.or(
                        cb.isFalse(root.get("isDlc"))
                );
    }

    /**
     * Returns a specification based on the provided value, if present
     * @param value
     * @param specFunc
     * @return
     * @param <T>
     */
    private static <T> Specification<GamesEntity> ifPresent(T value, Function<T, Specification<GamesEntity>> specFunc) {
        if (value == null) {
            return Specification.unrestricted();
        }

        if (value instanceof String stringValue && stringValue.isBlank()) {
            return Specification.unrestricted();
        }

        return specFunc.apply(value);
    }
}
