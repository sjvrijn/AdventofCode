using AdventofCode
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
            @test AdventofCode.day01.a(data) == result
        end
    end

    @testset "Day 1, part 2" begin
        testfiles = Dict(
            "input01-test1.txt" => 142,
            "input01-test2.txt" => 281,
        )
        for (file, result) in testfiles
            data = readlines(joinpath(INPUT, file))
            @test AdventofCode.day01.b(data) == result
        end
    end

end

@testset "Day 2" begin

    @testset "Day 2, part 1" begin
        testfiles = Dict(
            "input02-test1.txt" => 8,
        )
        for (file, result) in testfiles
            data = AdventofCode.day02.parse_file(joinpath(INPUT, file))
            @test AdventofCode.day02.a(data) == result
        end
    end

    @testset "Day 2, part 2" begin
        testfiles = Dict(
            "input02-test1.txt" => 2286,
        )
        for (file, result) in testfiles
            data = AdventofCode.day02.parse_file(joinpath(INPUT, file))
            @test AdventofCode.day02.b(data) == result
        end
    end

end