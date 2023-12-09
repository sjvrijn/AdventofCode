using AdventofCode: day01, day02, day03, day04
using Test

const INPUT = joinpath(@__DIR__, "../inputs")

@testset "Day 1" begin

    @testset "Day 1, part 1" begin
        testfiles = Dict(
            "input01-test1.txt" => 142,
            "input01-test2.txt" => 209,
        )
        for (file, result) in testfiles
            data = readlines(joinpath(INPUT, file))
            @test day01.a(data) == result
        end
    end

    @testset "Day 1, part 2" begin
        testfiles = Dict(
            "input01-test1.txt" => 142,
            "input01-test2.txt" => 281,
        )
        for (file, result) in testfiles
            data = readlines(joinpath(INPUT, file))
            @test day01.b(data) == result
        end
    end

end

@testset "Day 2" begin

    @testset "Day 2, part 1" begin
        testfiles = Dict(
            "input02-test1.txt" => 8,
        )
        for (file, result) in testfiles
            data = day02.parse_file(joinpath(INPUT, file))
            @test day02.a(data) == result
        end
    end

    @testset "Day 2, part 2" begin
        testfiles = Dict(
            "input02-test1.txt" => 2286,
        )
        for (file, result) in testfiles
            data = day02.parse_file(joinpath(INPUT, file))
            @test day02.b(data) == result
        end
    end

end

@testset "Day 3" begin

    @testset "Day 3, part 1" begin
        testfiles = Dict(
            "input03-test1.txt" => 4361,
        )
        for (file, result) in testfiles
            data = day03.parse_file(joinpath(INPUT, file))
            @test day03.a(data) == result
        end
    end

    @testset "Day 3, part 2" begin
        testfiles = Dict(
            "input03-test1.txt" => 467835,
        )
        for (file, result) in testfiles
            data = day03.parse_file(joinpath(INPUT, file))
            @test day03.b(data) == result
        end
    end

end

@testset "Day 4" begin

    @testset "Day 4, part 1" begin
        testfiles = Dict(
            "input04-test1.txt" => 13,
        )
        for (file, result) in testfiles
            data = day04.parse_file(joinpath(INPUT, file))
            @test day04.a(data) == result
        end
    end

    @testset "Day 4, part 2" begin
        testfiles = Dict(
            "input04-test1.txt" => 30,
        )
        for (file, result) in testfiles
            data = day04.parse_file(joinpath(INPUT, file))
            @test day04.b(data) == result
        end
    end

end