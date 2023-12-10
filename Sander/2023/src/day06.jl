module day06
function a(data)
    times, distances = data
    num_ways = 1
    for (time, distance) in zip(times, distances)
        press = 1
        while press*(time-press) <= distance
            press += 1
        end
        num_ways *= (time+1) - 2*press
    end
    return prod(num_ways)
end


function b(data)
    time, distance = parse(Int, join(data[1])), parse(Int, join(data[2]))

    press = 1
    while press*(time-press) <= distance
        press += 1
    end

    return (time+1) - 2*press
end


function parse_file(path)
    lines = readlines(joinpath(@__DIR__, path))
    times = map(x -> parse(Int, x), split(lines[1])[2:end])
    distances = map(x -> parse(Int, x), split(lines[2])[2:end])
    return times, distances
end


function both()
    data = parse_file("../inputs/input06.txt")
    println(a(data))
    println(b(data))
end

end
