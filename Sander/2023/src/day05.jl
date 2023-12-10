module day05

struct MapRange
    start::Int
    stop::Int
    offset::Int

    function MapRange(numbers)
        to_start, from_start, range_length = numbers
        new(from_start, from_start+range_length, to_start - from_start)
    end
end


function contains(map_range::MapRange, value::Int)
    return map_range.start <= value < map_range.stop
end


function a(data)
    seeds, translation_map, maps = data
    cur_map = "seed"

    while cur_map != "location"
        cur_map = translation_map[cur_map]
        new_values = []
        for (i, seed) in enumerate(seeds)
            new_value = nothing
            for map_range in maps[cur_map]
                if contains(map_range, seed)
                    new_value = seed + map_range.offset
                    break
                end
            end
            if isnothing(new_value)
                new_value = seed
            end
            append!(new_values, new_value)
        end
        seeds = new_values
    end

    return minimum(seeds)
end


"""
    contains(map_range::MapRange, seed_range::UnitRange)

Determines if a `map_range` matches a `seed_range`.

This happens in the following cases:

       |--------map_range-------|
    |--seed_range--|
    |-----------seed_range----------|
                   |---seed_range---|
             |--seed_range--|
"""
function contains(map_range::MapRange, seed_range::UnitRange)
    return (seed_range.start <= map_range.start < seed_range.stop
            || seed_range.start < map_range.stop <= seed_range.stop
            || (seed_range.start >= map_range.start && seed_range.stop <= map_range.stop))
end

"""
    translate_seed_range(seed_range, map_range)

Perform the mapping of `map_range` on `seed_range`.
Assumes contains(map_range, seed_range) is true.
"""
function translate_seed_range(seed_range, map_range)

    mapped_ranges = []
    # map (i.e. cut off) the seed range leading up to the map range
    if seed_range.start < map_range.start < seed_range.stop
        append!(mapped_ranges, [seed_range.start:map_range.start])
        seed_range = map_range.start:seed_range.stop
    end

    # map the overlapping part of the seed range
    contained_range = seed_range.start:min(seed_range.stop, map_range.stop)
    mapped_range = (contained_range.start + map_range.offset):(contained_range.stop + map_range.offset)
    append!(mapped_ranges, [mapped_range])
    # cut off the potential seed range at the end for further processing
    if map_range.stop < seed_range.stop
        seed_range = map_range.stop:seed_range.stop
    else
        seed_range = nothing
    end

    return mapped_ranges, seed_range

end


function merge_ranges(ranges)
    merged_ranges = []
    sort!(ranges)
    cur_range = first(ranges)

    for range in ranges[2:end]
        if range.stop <= cur_range.stop
            continue
        elseif range.start <= cur_range.stop
            cur_range = cur_range.start:range.stop
        elseif range.start > cur_range.stop
            append!(merged_ranges, [cur_range])
            cur_range = range
        end
    end
    # don't forget to add the final range
    append!(merged_ranges, [cur_range])
    return merged_ranges
end


function b(data)
    seed_ranges, translation_map, maps = data
    seed_ranges = [
        seed_start:(seed_start+seed_length)
        for (seed_start, seed_length) in zip(seed_ranges[1:2:end], seed_ranges[2:2:end])
    ]
    cur_map = "seed"

    while cur_map != "location"
        cur_map = translation_map[cur_map]
        new_ranges = []
        for seed_range in seed_ranges
            for map_range in maps[cur_map]
                if !contains(map_range, seed_range)
                    continue
                end
                mapped, seed_range = translate_seed_range(seed_range, map_range)
                append!(new_ranges, mapped)
                if isnothing(seed_range)
                    break
                end
            end
            if !isnothing(seed_range)
                # Add any remaining seed_range
                append!(new_ranges, [seed_range])
            end
        end
        seed_ranges = merge_ranges(new_ranges)
    end

    return first(seed_ranges).start
end


function parse_file(path)
    lines = readlines(joinpath(@__DIR__, path))
    seeds = map(x -> parse(Int, x), split(lines[1])[2:end])

    maps, translation_map = Dict(), Dict()
    cur_map = ""
    for line in lines[3:end]
        if cur_map == ""
            from, to = split(split(line)[1], "-")[[1,3]]
            translation_map[from] = to
            cur_map = to
            maps[to] = []
        elseif line == ""
            cur_map = ""
        else
            numbers = map(x -> parse(Int, x), split(line))
            append!(maps[cur_map], [MapRange(numbers)])
        end
    end

    for map_ranges in values(maps)
        sort!(map_ranges, by=x -> x.start)
    end

    return seeds, translation_map, maps
end


function both()
    data = parse_file("../inputs/input05.txt")
    println(a(data))
    println(b(data))
end

end
