using AdventofCode: day05

@testset "Day 5" begin

    @testset "Day 5, part 1" begin
        testfiles = Dict(
            "input05-test1.txt" => 35,
        )
        for (file, result) in testfiles
            data = day05.parse_file(joinpath(INPUT, file))
            @test day05.a(data) == result
        end
    end

    @testset "Day 5 helpers" begin

        @testset "Day 5 helper: contains(map_range, seed_range)" begin
            map_range = day05.MapRange([10, 5, 5])  # 5:10, offset 5
            @test !day05.contains(map_range, 1:5)
            @test !day05.contains(map_range, 10:14)

            @test day05.contains(map_range, 1:6)
            @test day05.contains(map_range, 1:16)
            @test day05.contains(map_range, 6:16)
            @test day05.contains(map_range, 6:9)
        end

        @testset "Day 5 helper: translate_seed_range" begin
            map_range = day05.MapRange([10, 5, 5])  # 5:10, offset 5

            mapped, seed = day05.translate_seed_range(1:7, map_range)
            @test mapped == [1:5, 10:12]
            @test isnothing(seed)

            mapped, seed = day05.translate_seed_range(7:12, map_range)
            @test mapped == [12:15]
            @test seed == 10:12

            mapped, seed = day05.translate_seed_range(1:12, map_range)
            @test mapped == [1:5, 10:15]
            @test seed == 10:12

            mapped, seed = day05.translate_seed_range(5:12, map_range)
            @test mapped == [10:15]
            @test seed == 10:12
        end

        @testset "Day 5 helper: merge_ranges" begin
            @test day05.merge_ranges([1:5, 5:10]) == [1:10]
            @test day05.merge_ranges([1:10, 2:9]) == [1:10]
            @test day05.merge_ranges([1:5, 6:10]) == [1:5, 6:10]
            @test day05.merge_ranges([20:25, 10:15, 7:12, 3:9, 1:5]) == [1:15, 20:25]
        end
    end

    @testset "Day 5, part 2" begin
        testfiles = Dict(
            "input05-test1.txt" => 46,
        )
        for (file, result) in testfiles
            data = day05.parse_file(joinpath(INPUT, file))
            @test day05.b(data) == result
        end
    end

end