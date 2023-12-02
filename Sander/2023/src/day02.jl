module day02

function a(data)
    max_cubes = [12, 13, 14]
    total = sum(
        i for (i, game_set) in enumerate(data)
        if !any(sum(game .> max_cubes) > 0 for game in game_set)
    )
    return total
end

function b(data)
    total = sum(
        prod(maximum(reduce(hcat, game_set), dims=2))
        for game_set in data
    )
    # total = 0
    # for game_set in data
    #     power = prod(maximum(reduce(hcat, game_set), dims=2))
    #     println("$power : $game_set")
    #     total += power
    # end

    return total
end

function parse_set(cube_set)
    indices = Dict("red" => 1, "green" => 2, "blue" => 3)
    num_cubes = [0, 0, 0]
    for cube in split(cube_set, ", ")
        num, color = split(cube, " ")
        num_cubes[indices[color]] = parse(Int, num)
    end
    return num_cubes
end

function parse_file(path)
    lines = readlines(joinpath(@__DIR__, path))
    games = []
    for line in lines
        _, sets = split(line, ": ")
        append!(games, [[parse_set(cube_set) for cube_set in split(sets, "; ")]])
    end
    return games
end

function both()
    data = parse_file("../inputs/input02.txt")
    println(a(data))
    println(b(data))
end

end
