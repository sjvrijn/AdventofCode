module day01

function a(data)
    total = 0
    for line in data
        first, last = 0, 0
        for char in line
            if !contains("123456789", char)
                continue
            else
                val = Int(char) - 48
            end
            if first == 0
                first = val * 10
            end
            last = val
        end
        total += first + last
    end
    return total
end

function b(data)
    translate = Dict(
        "1" => 1, "2" => 2, "3" => 3,
        "4" => 4, "5" => 5, "6" => 6,
        "7" => 7, "8" => 8, "9" => 9,
        "one" => 1, "two" => 2, "three" => 3,
        "four" => 4, "five" => 5, "six" => 6,
        "seven" => 7, "eight" => 8, "nine" => 9,
    )
    total = 0
    for line in data
        values = []
        for start in 0:(length(line)-1)
            for num_chars in [1, 3, 4, 5]
                to_check = first(chop(line, head=start, tail=0), num_chars)
                if !(haskey(translate, to_check))
                    continue
                end
                append!(values, translate[to_check])
            end
        end
        total += (values[1] * 10 + values[end])
    end
    return total
end

function both()
    data = readlines(joinpath(@__DIR__, "../inputs/input01.txt"))
    println(a(data))
    println(b(data))
end

end
